from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse
from datetime import timedelta

from inventory.models import Barang, Kategori, Satuan
from transactions.models import BarangMasuk, BarangKeluar, StokBatch, BarangKeluarBatch


class FIFOTransactionTestCase(TestCase):
    def setUp(self):
        self.kategori = Kategori.objects.create(nama="Bahan Dapur", deskripsi="Bahan makanan")
        self.satuan = Satuan.objects.create(nama="Kg")
        
        # 1. Test auto-initial stock creation on new Barang
        self.barang = Barang.objects.create(
            nama="Bawang Bombay",
            kategori=self.kategori,
            satuan=self.satuan,
            stok_minimal=5,
            stok_saat_ini=10  # This should trigger auto creation of BarangMasuk & StokBatch
        )
        
        # Admin User for client testing
        from django.contrib.auth.models import User
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
        self.client = Client()
        self.client.force_login(self.user)

    def test_auto_stock_awal(self):
        # Verify that auto-initial stock is generated
        self.assertEqual(self.barang.stok_saat_ini, 10)
        
        # Should create a BarangMasuk with "Sistem (Stok Awal)"
        bm = BarangMasuk.objects.filter(barang=self.barang, supplier="Sistem (Stok Awal)").first()
        self.assertIsNotNone(bm)
        self.assertEqual(bm.jumlah, 10)
        
        # Should also create corresponding StokBatch
        batch = StokBatch.objects.filter(barang_masuk=bm).first()
        self.assertIsNotNone(batch)
        self.assertEqual(batch.jumlah_sekarang, 10)

    def test_barang_masuk_creates_stok_batch(self):
        # Create new BarangMasuk
        today = timezone.now().date()
        exp_date = today + timedelta(days=30)
        bm = BarangMasuk.objects.create(
            barang=self.barang,
            jumlah=20,
            supplier="Toko Sayur",
            tanggal=today,
            tanggal_kadaluarsa=exp_date
        )
        
        # Verify StokBatch
        batch = StokBatch.objects.filter(barang_masuk=bm).first()
        self.assertIsNotNone(batch)
        self.assertEqual(batch.jumlah_awal, 20)
        self.assertEqual(batch.jumlah_sekarang, 20)
        self.assertEqual(batch.tanggal_kadaluarsa, exp_date)
        
        # Verify global stock
        self.barang.refresh_from_db()
        self.assertEqual(self.barang.stok_saat_ini, 30)

    def test_fifo_deduction_basic(self):
        # Create a second batch that expires earlier
        today = timezone.now().date()
        bm_early = BarangMasuk.objects.create(
            barang=self.barang,
            jumlah=15,
            supplier="Toko Bumbu",
            tanggal=today,
            tanggal_kadaluarsa=today + timedelta(days=5)  # Expires in 5 days (earliest)
        )
        
        # Current stock is 10 (Sistem Stok Awal, no expiry) + 15 (expires in 5 days) = 25
        self.barang.refresh_from_db()
        self.assertEqual(self.barang.stok_saat_ini, 25)
        
        # Create BarangKeluar
        bk = BarangKeluar.objects.create(
            barang=self.barang,
            jumlah=5,
            alasan=BarangKeluar.Alasan.PEMAKAIAN_DAPUR,
            tanggal=today
        )
        
        # FIFO should deduct from bm_early first because its expiry is earliest (5 days vs Null)
        batch_early = bm_early.batch
        batch_early.refresh_from_db()
        self.assertEqual(batch_early.jumlah_sekarang, 10)  # 15 - 5 = 10
        
        # Check junction
        junction = BarangKeluarBatch.objects.filter(barang_keluar=bk).first()
        self.assertEqual(junction.stok_batch, batch_early)
        self.assertEqual(junction.jumlah, 5)

    def test_fifo_multiple_batches(self):
        today = timezone.now().date()
        # Batch 2: Expires in 5 days
        bm_early = BarangMasuk.objects.create(
            barang=self.barang,
            jumlah=5,
            supplier="Toko Bumbu",
            tanggal=today,
            tanggal_kadaluarsa=today + timedelta(days=5)
        )
        
        # We have Batch 1 (Stok awal: 10, no expiry) and Batch 2 (5, expires in 5 days)
        # Deduct 8 items. This should fully consume Batch 2 (5) and then consume 3 from Batch 1
        bk = BarangKeluar.objects.create(
            barang=self.barang,
            jumlah=8,
            alasan=BarangKeluar.Alasan.PEMAKAIAN_DAPUR,
            tanggal=today
        )
        
        bm_early.batch.refresh_from_db()
        self.assertEqual(bm_early.batch.jumlah_sekarang, 0)  # Fully consumed
        
        # Stok awal batch (Batch 1)
        initial_bm = BarangMasuk.objects.get(supplier="Sistem (Stok Awal)")
        initial_bm.batch.refresh_from_db()
        self.assertEqual(initial_bm.batch.jumlah_sekarang, 7)  # 10 - 3 = 7
        
        # Verify junctions count
        junctions = BarangKeluarBatch.objects.filter(barang_keluar=bk)
        self.assertEqual(junctions.count(), 2)

    def test_fifo_sorting_expiry_null_last(self):
        today = timezone.now().date()
        # Batch 1 (Stok Awal) has no expiry (Null).
        # Batch 2 has expiry in 50 days.
        bm_late = BarangMasuk.objects.create(
            barang=self.barang,
            jumlah=10,
            supplier="Supplier B",
            tanggal=today,
            tanggal_kadaluarsa=today + timedelta(days=50)
        )
        
        # Deduct 5. Since Batch 2 expires in 50 days (not Null) and Batch 1 (Stok Awal) is Null,
        # FIFO should deduct from Batch 2 first.
        bk = BarangKeluar.objects.create(
            barang=self.barang,
            jumlah=5,
            alasan=BarangKeluar.Alasan.PEMAKAIAN_DAPUR,
            tanggal=today
        )
        
        bm_late.batch.refresh_from_db()
        self.assertEqual(bm_late.batch.jumlah_sekarang, 5)  # 10 - 5 = 5
        
        initial_bm = BarangMasuk.objects.get(supplier="Sistem (Stok Awal)")
        initial_bm.batch.refresh_from_db()
        self.assertEqual(initial_bm.batch.jumlah_sekarang, 10)  # Untouched because it is Null expiry (placed last)

    def test_validation_error_exceeds_stock(self):
        today = timezone.now().date()
        # Stock is 10. Deducting 15 should raise ValidationError.
        bk = BarangKeluar(
            barang=self.barang,
            jumlah=15,
            alasan=BarangKeluar.Alasan.PEMAKAIAN_DAPUR,
            tanggal=today
        )
        with self.assertRaises(ValidationError):
            bk.clean()

    def test_delete_barang_keluar_restores_batch(self):
        today = timezone.now().date()
        # Create a checkout transaction of 4 items
        bk = BarangKeluar.objects.create(
            barang=self.barang,
            jumlah=4,
            alasan=BarangKeluar.Alasan.PEMAKAIAN_DAPUR,
            tanggal=today
        )
        
        initial_bm = BarangMasuk.objects.get(supplier="Sistem (Stok Awal)")
        initial_bm.batch.refresh_from_db()
        self.assertEqual(initial_bm.batch.jumlah_sekarang, 6)  # 10 - 4 = 6
        
        # Delete transaction
        bk.delete()
        
        # Verify restored stock
        initial_bm.batch.refresh_from_db()
        self.assertEqual(initial_bm.batch.jumlah_sekarang, 10)
        self.barang.refresh_from_db()
        self.assertEqual(self.barang.stok_saat_ini, 10)

    def test_update_barang_keluar_restores_and_rededucts(self):
        today = timezone.now().date()
        # Deduct 4 items
        bk = BarangKeluar.objects.create(
            barang=self.barang,
            jumlah=4,
            alasan=BarangKeluar.Alasan.PEMAKAIAN_DAPUR,
            tanggal=today
        )
        
        initial_bm = BarangMasuk.objects.get(supplier="Sistem (Stok Awal)")
        initial_bm.batch.refresh_from_db()
        self.assertEqual(initial_bm.batch.jumlah_sekarang, 6)
        
        # Update quantity to 6
        bk.jumlah = 6
        bk.save()
        
        initial_bm.batch.refresh_from_db()
        self.assertEqual(initial_bm.batch.jumlah_sekarang, 4)  # 10 - 6 = 4
        self.barang.refresh_from_db()
        self.assertEqual(self.barang.stok_saat_ini, 4)

    def test_delete_barang_masuk_guard(self):
        today = timezone.now().date()
        # Batch 2: 5 items
        bm_early = BarangMasuk.objects.create(
            barang=self.barang,
            jumlah=5,
            supplier="Toko Bumbu",
            tanggal=today,
            tanggal_kadaluarsa=today + timedelta(days=5)
        )
        
        # Consume 2 items (deducted from bm_early first)
        BarangKeluar.objects.create(
            barang=self.barang,
            jumlah=2,
            alasan=BarangKeluar.Alasan.PEMAKAIAN_DAPUR,
            tanggal=today
        )
        
        # Deleting bm_early should fail since 2 of its items are consumed
        with self.assertRaises(ValidationError):
            bm_early.delete()

    def test_ledger_list_view_and_exports(self):
        # Ledger Page
        url = reverse('transactions:ledger_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sistem (Stok Awal)")
        
        # Filter request
        response_filtered = self.client.get(url, {'q': 'Bawang'})
        self.assertEqual(response_filtered.status_code, 200)
        
        # Export CSV
        url_csv = reverse('transactions:ledger_csv')
        response_csv = self.client.get(url_csv)
        self.assertEqual(response_csv.status_code, 200)
        self.assertEqual(response_csv['Content-Type'], 'text/csv; charset=utf-8-sig')
        
        # Export PDF
        url_pdf = reverse('transactions:ledger_pdf')
        response_pdf = self.client.get(url_pdf)
        self.assertEqual(response_pdf.status_code, 200)
        self.assertEqual(response_pdf['Content-Type'], 'application/pdf')
