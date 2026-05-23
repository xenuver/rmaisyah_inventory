from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from inventory.models import Barang, Kategori, Satuan
from transactions.models import BarangMasuk, BarangKeluar, StokBatch, BarangKeluarBatch


class InventoryTransactionTestCase(TestCase):
    def setUp(self):
        self.kategori = Kategori.objects.create(nama="Bahan Dapur", deskripsi="Bumbu dan sayuran")
        self.satuan = Satuan.objects.create(nama="Kg")

    def test_barang_creation_initial_stock(self):
        """
        Memastikan pembuatan Barang dengan stok_saat_ini > 0 otomatis
        membuat transaksi BarangMasuk dan StokBatch sebagai 'Stok Awal'.
        """
        barang = Barang.objects.create(
            nama="Bawang Merah",
            kategori=self.kategori,
            satuan=self.satuan,
            stok_minimal=5,
            stok_saat_ini=10
        )
        
        # Validasi stok awal di-cache dengan benar
        self.assertEqual(barang.stok_saat_ini, 10)
        
        # Harus ada 1 transaksi BarangMasuk
        masuk = BarangMasuk.objects.filter(barang=barang)
        self.assertEqual(masuk.count(), 1)
        self.assertEqual(masuk.first().jumlah, 10)
        self.assertEqual(masuk.first().supplier, 'Sistem (Stok Awal)')
        
        # Harus ada 1 batch dengan sisa stok 10
        self.assertEqual(barang.batches.count(), 1)
        self.assertEqual(barang.batches.first().stok_sisa, 10)

    def test_barang_masuk_creates_batch(self):
        """
        Memastikan pencatatan BarangMasuk menambah stok dan membuat StokBatch baru.
        """
        barang = Barang.objects.create(
            nama="Bawang Putih",
            kategori=self.kategori,
            satuan=self.satuan,
            stok_minimal=5,
            stok_saat_ini=0
        )
        
        # Input barang masuk
        masuk = BarangMasuk.objects.create(
            barang=barang,
            jumlah=15,
            supplier="Supplier A",
            tanggal=timezone.now().date(),
            tanggal_kadaluarsa=timezone.now().date() + timedelta(days=10)
        )
        
        # Validasi update stok
        barang.refresh_from_db()
        self.assertEqual(barang.stok_saat_ini, 15)
        
        # Validasi batch
        self.assertEqual(barang.batches.count(), 1)
        batch = barang.batches.first()
        self.assertEqual(batch.stok_sisa, 15)
        self.assertEqual(batch.tanggal_kadaluarsa, masuk.tanggal_kadaluarsa)

    def test_barang_keluar_fifo_order(self):
        """
        Memastikan pengurangan stok secara FIFO: memotong batch terlama (expiring first).
        """
        barang = Barang.objects.create(
            nama="Cabai Rawit",
            kategori=self.kategori,
            satuan=self.satuan,
            stok_minimal=5,
            stok_saat_ini=0
        )
        
        # Batch 1: Kadaluarsa 5 hari lagi (Quantity: 10)
        masuk1 = BarangMasuk.objects.create(
            barang=barang,
            jumlah=10,
            tanggal=timezone.now().date(),
            tanggal_kadaluarsa=timezone.now().date() + timedelta(days=5)
        )
        
        # Batch 2: Kadaluarsa 10 hari lagi (Quantity: 20)
        masuk2 = BarangMasuk.objects.create(
            barang=barang,
            jumlah=20,
            tanggal=timezone.now().date(),
            tanggal_kadaluarsa=timezone.now().date() + timedelta(days=10)
        )
        
        # Total stok = 30
        barang.refresh_from_db()
        self.assertEqual(barang.stok_saat_ini, 30)
        
        # Catat Barang Keluar: 15
        # FIFO harus memotong: 10 dari Batch 1 (habis), dan 5 dari Batch 2 (tersisa 15)
        keluar = BarangKeluar.objects.create(
            barang=barang,
            jumlah=15,
            tanggal=timezone.now().date()
        )
        
        # Validasi stok akhir
        barang.refresh_from_db()
        self.assertEqual(barang.stok_saat_ini, 15)
        
        # Verifikasi sisa batch di database
        batch1 = masuk1.batch
        batch1.refresh_from_db()
        self.assertEqual(batch1.stok_sisa, 0)
        
        batch2 = masuk2.batch
        batch2.refresh_from_db()
        self.assertEqual(batch2.stok_sisa, 15)
        
        # Verifikasi audit pemotongan batch
        deductions = keluar.batch_deductions.all().order_by('jumlah')
        self.assertEqual(deductions.count(), 2)
        self.assertEqual(deductions.first().jumlah, 5)  # dari Batch 2
        self.assertEqual(deductions.last().jumlah, 10)  # dari Batch 1

    def test_barang_keluar_validation_insufficient_stock(self):
        """
        Memastikan ValidationError dilempar jika stok keluar melebihi stok tersedia.
        """
        barang = Barang.objects.create(
            nama="Garam",
            kategori=self.kategori,
            satuan=self.satuan,
            stok_minimal=5,
            stok_saat_ini=5
        )
        
        keluar = BarangKeluar(
            barang=barang,
            jumlah=10, # Melebihi stok yang ada (5)
            tanggal=timezone.now().date()
        )
        
        with self.assertRaises(ValidationError):
            keluar.clean()

    def test_barang_keluar_revert_on_delete(self):
        """
        Memastikan stok batch dan stok master kembali pulih jika transaksi keluar dihapus.
        """
        barang = Barang.objects.create(
            nama="Kecap",
            kategori=self.kategori,
            satuan=self.satuan,
            stok_minimal=5,
            stok_saat_ini=10
        )
        
        # Ketersediaan awal: batch sisa = 10, total stok = 10
        keluar = BarangKeluar.objects.create(
            barang=barang,
            jumlah=4,
            tanggal=timezone.now().date()
        )
        
        # Setelah keluar 4: total = 6, batch sisa = 6
        barang.refresh_from_db()
        self.assertEqual(barang.stok_saat_ini, 6)
        self.assertEqual(barang.batches.first().stok_sisa, 6)
        
        # Hapus transaksi keluar
        keluar.delete()
        
        # Harus kembali ke 10
        barang.refresh_from_db()
        self.assertEqual(barang.stok_saat_ini, 10)
        self.assertEqual(barang.batches.first().stok_sisa, 10)

    def test_barang_keluar_revert_on_update(self):
        """
        Memastikan update jumlah barang keluar menghitung ulang FIFO dengan benar.
        """
        barang = Barang.objects.create(
            nama="Minyak Goreng",
            kategori=self.kategori,
            satuan=self.satuan,
            stok_minimal=5,
            stok_saat_ini=20
        )
        
        # Catat Barang Keluar awal: 5
        keluar = BarangKeluar.objects.create(
            barang=barang,
            jumlah=5,
            tanggal=timezone.now().date()
        )
        
        barang.refresh_from_db()
        self.assertEqual(barang.stok_saat_ini, 15)
        self.assertEqual(barang.batches.first().stok_sisa, 15)
        
        # Edit Barang Keluar menjadi: 12
        keluar.jumlah = 12
        keluar.clean()
        keluar.save()
        
        barang.refresh_from_db()
        self.assertEqual(barang.stok_saat_ini, 8)
        self.assertEqual(barang.batches.first().stok_sisa, 8)

    def test_barang_masuk_delete_validation(self):
        """
        Memastikan transaksi masuk tidak bisa dihapus jika stok dari batch tersebut
        sudah mulai digunakan oleh transaksi keluar.
        """
        barang = Barang.objects.create(
            nama="Tomat",
            kategori=self.kategori,
            satuan=self.satuan,
            stok_minimal=2,
            stok_saat_ini=0
        )
        
        masuk = BarangMasuk.objects.create(
            barang=barang,
            jumlah=10,
            tanggal=timezone.now().date()
        )
        
        # Gunakan sebagian stok (3)
        BarangKeluar.objects.create(
            barang=barang,
            jumlah=3,
            tanggal=timezone.now().date()
        )
        
        # Mencoba menghapus BarangMasuk harus gagal karena stok sisa (7) < stok awal (10)
        with self.assertRaises(ValidationError):
            masuk.delete()

    def test_ledger_list_view_authenticated(self):
        """
        Memastikan halaman Ledger dapat diakses dengan sukses (200 OK) oleh user terautentikasi.
        """
        from django.contrib.auth.models import User
        user = User.objects.create_user(username="admin_test", password="password123")
        self.client.login(username="admin_test", password="password123")
        
        # Buat barang masuk agar ada data ledger
        Barang.objects.create(
            nama="Merica",
            kategori=self.kategori,
            satuan=self.satuan,
            stok_minimal=1,
            stok_saat_ini=5
        )
        
        response = self.client.get('/transactions/ledger/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('ledger_entries', response.context)
        # Harus ada minimal 1 entri (stok awal Merica)
        self.assertTrue(len(response.context['ledger_entries']) >= 1)

    def test_export_ledger_csv_authenticated(self):
        """
        Memastikan export CSV mengembalikan response file download (200 OK)
        dan struktur datanya sesuai.
        """
        from django.contrib.auth.models import User
        User.objects.create_user(username="admin_test", password="password123")
        self.client.login(username="admin_test", password="password123")
        
        # Buat barang masuk agar ada data ledger
        Barang.objects.create(
            nama="Gula",
            kategori=self.kategori,
            satuan=self.satuan,
            stok_minimal=1,
            stok_saat_ini=10
        )
        
        response = self.client.get('/transactions/ledger/export/csv/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8-sig')
        # Content-Disposition harus menyertakan nama file
        self.assertIn('attachment; filename="ledger_inventaris.csv"', response['Content-Disposition'])
        
        # Verifikasi isi (header)
        content = response.content.decode('utf-8-sig')
        self.assertIn('Tanggal;Tipe;Nama Barang;Jumlah;Satuan;Keterangan Transaksi;Catatan', content)
        # Harus ada data Gula
        self.assertIn('Gula', content)

    def test_ledger_print_view_authenticated(self):
        """
        Memastikan halaman print laporan buku besar dapat dimuat dengan baik.
        """
        from django.contrib.auth.models import User
        User.objects.create_user(username="admin_test", password="password123")
        self.client.login(username="admin_test", password="password123")
        
        response = self.client.get('/transactions/ledger/print/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename="ledger_inventaris.pdf"', response['Content-Disposition'])


