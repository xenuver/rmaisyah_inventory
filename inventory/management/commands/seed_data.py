from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from inventory.models import Kategori, Satuan, Barang
from transactions.models import BarangMasuk, BarangKeluar, StokBatch, BarangKeluarBatch

class Command(BaseCommand):
    help = 'Seed database with dummy data for Rumah Makan Aisyah'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing existing data...')
        
        # Hapus data lama secara berurutan untuk menghindari ProtectedError
        BarangKeluarBatch.objects.all().delete()
        StokBatch.objects.all().delete()
        BarangMasuk.objects.all().delete()
        BarangKeluar.objects.all().delete()
        Barang.objects.all().delete()
        Kategori.objects.all().delete()
        Satuan.objects.all().delete()

        self.stdout.write('Seeding fresh data...')

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

        # 3. Barang (Stok saat ini diatur 0, pengisian akan melalui transaksi masuk)
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
            obj = Barang.objects.create(
                nama=nama,
                kategori=kat_objs[kat_nama],
                satuan=sat_objs[sat_nama],
                stok_minimal=min_stok,
                stok_saat_ini=0
            )
            barang_objs.append(obj)

        self.stdout.write(f'Created {len(kategoris)} Kategori, {len(satuans)} Satuan, {len(barangs_data)} Barang')

        # 4. Generate Events (Masuk & Keluar) over the last 30 days
        now = timezone.now()
        suppliers = ['PT. Pangan Makmur', 'Toko Sembako Abadi', 'Pasar Tradisional Induk', 'Agen Telur Berkah']
        
        events = []
        # Generate 120 incoming events
        for _ in range(120):
            days_ago = random.randint(0, 30)
            tgl = (now - timedelta(days=days_ago)).date()
            events.append({
                'type': 'masuk',
                'tanggal': tgl,
            })
            
        # Generate 250 outgoing events
        for _ in range(250):
            days_ago = random.randint(0, 30)
            tgl = (now - timedelta(days=days_ago)).date()
            events.append({
                'type': 'keluar',
                'tanggal': tgl,
            })
            
        # Urutkan kronologis (sangat penting untuk kestabilan logika stok dan FIFO)
        events.sort(key=lambda x: x['tanggal'])

        self.stdout.write(f'Generated {len(events)} events. Processing chronologically...')
        
        masuk_count = 0
        keluar_count = 0

        for ev in events:
            tgl = ev['tanggal']
            b = random.choice(barang_objs)
            
            if ev['type'] == 'masuk':
                qty = random.randint(15, 80)
                exp_date = None
                if b.kategori.nama in ['Bahan Pokok', 'Minuman', 'Bumbu & Rempah']:
                    exp_date = tgl + timedelta(days=random.randint(14, 150))
                
                bm = BarangMasuk.objects.create(
                    barang=b,
                    jumlah=qty,
                    supplier=random.choice(suppliers),
                    keterangan='Restock pasokan dapur',
                    tanggal=tgl,
                    tanggal_kadaluarsa=exp_date
                )
                
                # Update created_at untuk visualisasi chart dan log yang rapi
                created_datetime = timezone.make_aware(
                    timezone.datetime.combine(tgl, timezone.datetime.min.time()) + 
                    timedelta(hours=random.randint(1, 23), minutes=random.randint(0, 59))
                )
                BarangMasuk.objects.filter(pk=bm.pk).update(created_at=created_datetime)
                if hasattr(bm, 'batch'):
                    bm.batch.created_at = created_datetime
                    bm.batch.save(update_fields=['created_at'])
                
                masuk_count += 1
            else:
                # Muat ulang dari db untuk mendapatkan sisa stok terkini
                b.refresh_from_db()
                if b.stok_saat_ini <= 0:
                    continue
                
                # Kurangi stok antara 1 s.d. sisa stok atau maks 15
                qty = random.randint(1, min(b.stok_saat_ini, 15))
                alasan = random.choices(
                    ['pemakaian_dapur', 'rusak', 'kadaluarsa', 'lainnya'], 
                    weights=[85, 5, 2, 8]
                )[0]
                
                bk = BarangKeluar.objects.create(
                    barang=b,
                    jumlah=qty,
                    alasan=alasan,
                    keterangan='Pemakaian masak harian' if alasan == 'pemakaian_dapur' else 'Pembersihan bahan rusak',
                    tanggal=tgl
                )
                
                created_datetime = timezone.make_aware(
                    timezone.datetime.combine(tgl, timezone.datetime.min.time()) + 
                    timedelta(hours=random.randint(1, 23), minutes=random.randint(0, 59))
                )
                BarangKeluar.objects.filter(pk=bk.pk).update(created_at=created_datetime)
                keluar_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded database! Created {masuk_count} incoming and {keluar_count} outgoing records.'
        ))
