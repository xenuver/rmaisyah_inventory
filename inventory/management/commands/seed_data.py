from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from inventory.models import Kategori, Satuan, Barang
from transactions.models import BarangMasuk, BarangKeluar

class Command(BaseCommand):
    help = 'Seed database with dummy data for Rumah Makan Aisyah'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # 1. Kategori
        kategoris = ['Bahan Pokok', 'Sayuran', 'Bumbu & Rempah', 'Daging & Ikan', 'Minuman', 'Alat Kebersihan', 'Lainnya']
        kat_objs = {}
        for k in kategoris:
            obj, _ = Kategori.objects.get_or_create(nama=k, defaults={'deskripsi': f'Kategori untuk {k.lower()}'})
            kat_objs[k] = obj

        # 2. Satuan
        satuans = ['Kg', 'Liter', 'Pcs', 'Ikat', 'Gram', 'Dus', 'Botol', 'Karung', 'Pack']
        sat_objs = {}
        for s in satuans:
            obj, _ = Satuan.objects.get_or_create(nama=s)
            sat_objs[s] = obj

        # 3. Barang
        barangs_data = [
            ('Beras Premium', 'Bahan Pokok', 'Kg', 50),
            ('Beras Biasa', 'Bahan Pokok', 'Kg', 50),
            ('Minyak Goreng', 'Bahan Pokok', 'Liter', 20),
            ('Tepung Terigu', 'Bahan Pokok', 'Kg', 10),
            ('Gula Pasir', 'Bahan Pokok', 'Kg', 15),
            ('Bawang Merah', 'Bumbu & Rempah', 'Kg', 5),
            ('Bawang Putih', 'Bumbu & Rempah', 'Kg', 5),
            ('Cabai Merah', 'Sayuran', 'Kg', 3),
            ('Cabai Rawit', 'Sayuran', 'Kg', 2),
            ('Ayam Potong', 'Daging & Ikan', 'Kg', 10),
            ('Daging Sapi', 'Daging & Ikan', 'Kg', 5),
            ('Telur Ayam', 'Daging & Ikan', 'Kg', 10),
            ('Ikan Nila', 'Daging & Ikan', 'Kg', 5),
            ('Tomat', 'Sayuran', 'Kg', 3),
            ('Wortel', 'Sayuran', 'Kg', 2),
            ('Kecap Manis', 'Bumbu & Rempah', 'Botol', 10),
            ('Saus Sambal', 'Bumbu & Rempah', 'Botol', 5),
            ('Garam', 'Bumbu & Rempah', 'Pack', 10),
            ('Merica Bubuk', 'Bumbu & Rempah', 'Pack', 20),
            ('Teh Celup', 'Minuman', 'Dus', 10),
            ('Kopi Bubuk', 'Minuman', 'Kg', 5),
            ('Es Batu', 'Minuman', 'Karung', 5),
            ('Sabun Cuci Piring', 'Alat Kebersihan', 'Liter', 5),
            ('Spons Cuci', 'Alat Kebersihan', 'Pcs', 10),
            ('Plastik Bungkus', 'Lainnya', 'Pack', 20),
        ]

        barang_objs = []
        for nama, kat_nama, sat_nama, min_stok in barangs_data:
            obj, created = Barang.objects.get_or_create(
                nama=nama,
                defaults={
                    'kategori': kat_objs[kat_nama],
                    'satuan': sat_objs[sat_nama],
                    'stok_minimal': min_stok,
                    'stok_saat_ini': 0,
                    'tanggal_kadaluarsa': timezone.now().date() + timedelta(days=random.randint(10, 180)) if kat_nama in ['Bahan Pokok', 'Minuman', 'Bumbu & Rempah'] else None
                }
            )
            if created:
                barang_objs.append(obj)
            else:
                barang_objs.append(obj)

        self.stdout.write(f'Created/Found {len(kategoris)} Kategori, {len(satuans)} Satuan, {len(barangs_data)} Barang')

        # 4. Generate Transactions (Masuk & Keluar) over the last 30 days
        now = timezone.now()
        suppliers = ['PT. Pangan Makmur', 'Toko Sembako Abadi', 'Pasar Tradisional Induk', 'Agen Telur Berkah']
        alasan_keluar = ['TERJUAL', 'DIPAKAI', 'RUSAK', 'KADALUARSA', 'LAINNYA']

        # Clear existing transactions to avoid piling up if run multiple times
        BarangMasuk.objects.all().delete()
        BarangKeluar.objects.all().delete()
        
        # Reset stok to 0
        for b in Barang.objects.all():
            b.stok_saat_ini = 0
            b.save()

        self.stdout.write('Generating transactions...')
        
        for _ in range(150): # 150 incoming transactions
            b = random.choice(barang_objs)
            days_ago = random.randint(0, 30)
            tgl = (now - timedelta(days=days_ago)).date()
            qty = random.randint(10, 100)
            
            bm = BarangMasuk.objects.create(
                barang=b,
                jumlah=qty,
                supplier=random.choice(suppliers),
                keterangan='Restock rutin',
                tanggal=tgl
            )
            # Override created_at
            bm.created_at = now - timedelta(days=days_ago, hours=random.randint(1, 10))
            bm.save()

        for _ in range(300): # 300 outgoing transactions
            b = random.choice(barang_objs)
            if b.stok_saat_ini <= 0:
                continue
            
            days_ago = random.randint(0, 30)
            tgl = (now - timedelta(days=days_ago)).date()
            
            # Ensure we don't go negative
            max_qty = min(b.stok_saat_ini, random.randint(1, 15))
            if max_qty == 0:
                continue
                
            alasan = random.choices(
                ['pemakaian_dapur', 'rusak', 'kadaluarsa', 'lainnya'], 
                weights=[70, 5, 5, 20]
            )[0]
            
            bk = BarangKeluar.objects.create(
                barang=b,
                jumlah=max_qty,
                alasan=alasan,
                keterangan='Penggunaan dapur harian' if alasan == 'pemakaian_dapur' else 'Lainnya',
                tanggal=tgl
            )
            bk.created_at = now - timedelta(days=days_ago, hours=random.randint(1, 10))
            bk.save()

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
