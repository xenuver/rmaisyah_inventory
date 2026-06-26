from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from inventory.models import Kategori, Satuan, Barang

User = get_user_model()


class Command(BaseCommand):
    help = (
        'Seed database dengan data awal untuk Rumah Makan Aisyah. '
        'Aman dijalankan berulang kali — data yang sudah ada tidak akan ditimpa.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-if-exists',
            action='store_true',
            help='Lewati seeding jika data sudah ada di database (default: selalu idempotent).',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Hapus semua data lama lalu seed ulang dari awal (BERBAHAYA di production!).',
        )

    def handle(self, *args, **kwargs):
        skip_if_exists = kwargs.get('skip_if_exists', False)
        force = kwargs.get('force', False)

        # ── Cek apakah data sudah ada ──────────────────────────────────────
        has_data = Kategori.objects.exists() or Satuan.objects.exists() or Barang.objects.exists()

        if has_data and skip_if_exists and not force:
            self.stdout.write(self.style.WARNING(
                'Data sudah ada di database. Seed dilewati (gunakan --force untuk seed ulang).'
            ))
            return

        if force:
            self.stdout.write(self.style.WARNING('--force aktif: Menghapus semua data lama...'))
            from transactions.models import BarangKeluarBatch, StokBatch, BarangMasuk, BarangKeluar
            BarangKeluarBatch.objects.all().delete()
            StokBatch.objects.all().delete()
            BarangMasuk.objects.all().delete()
            BarangKeluar.objects.all().delete()
            Barang.objects.all().delete()
            Kategori.objects.all().delete()
            Satuan.objects.all().delete()
            self.stdout.write('Data lama dihapus. Mulai seeding...')

        # ── 1. Kategori ────────────────────────────────────────────────────
        kategoris_data = [
            ('Bahan Pokok',    'Kategori untuk bahan pokok'),
            ('Sayuran',        'Kategori untuk sayuran'),
            ('Bumbu & Rempah', 'Kategori untuk bumbu & rempah'),
            ('Daging & Ikan',  'Kategori untuk daging & ikan'),
            ('Minuman',        'Kategori untuk minuman'),
            ('Alat Kebersihan','Kategori untuk alat kebersihan'),
            ('Lainnya',        'Kategori untuk lainnya'),
        ]
        kat_objs = {}
        kat_created = 0
        for nama, deskripsi in kategoris_data:
            obj, created = Kategori.objects.get_or_create(
                nama=nama,
                defaults={'deskripsi': deskripsi}
            )
            kat_objs[nama] = obj
            if created:
                kat_created += 1

        self.stdout.write(f'  Kategori: {kat_created} dibuat, {len(kategoris_data) - kat_created} sudah ada.')

        # ── 2. Satuan ──────────────────────────────────────────────────────
        satuans_data = ['Kg', 'Liter', 'Pcs', 'Ikat', 'Gram', 'Dus', 'Botol', 'Karung', 'Pack']
        sat_objs = {}
        sat_created = 0
        for nama in satuans_data:
            obj, created = Satuan.objects.get_or_create(nama=nama)
            sat_objs[nama] = obj
            if created:
                sat_created += 1

        self.stdout.write(f'  Satuan  : {sat_created} dibuat, {len(satuans_data) - sat_created} sudah ada.')

        # ── 3. Barang ──────────────────────────────────────────────────────
        # Format: (nama, kategori, satuan, stok_minimal)
        # stok_saat_ini tidak diisi di sini karena sudah dikelola melalui transaksi.
        barangs_data = [
            ('Beras Premium',     'Bahan Pokok',    'Kg',    50),
            ('Beras Biasa',       'Bahan Pokok',    'Kg',    50),
            ('Minyak Goreng',     'Bahan Pokok',    'Liter', 20),
            ('Tepung Terigu',     'Bahan Pokok',    'Kg',    10),
            ('Gula Pasir',        'Bahan Pokok',    'Kg',    15),
            ('Bawang Merah',      'Bumbu & Rempah', 'Kg',     5),
            ('Bawang Putih',      'Bumbu & Rempah', 'Kg',     5),
            ('Cabai Merah',       'Sayuran',        'Kg',     3),
            ('Cabai Rawit',       'Sayuran',        'Kg',     2),
            ('Ayam Potong',       'Daging & Ikan',  'Kg',    10),
            ('Daging Sapi',       'Daging & Ikan',  'Kg',     5),
            ('Telur Ayam',        'Daging & Ikan',  'Kg',    10),
            ('Ikan Nila',         'Daging & Ikan',  'Kg',     5),
            ('Tomat',             'Sayuran',        'Kg',     3),
            ('Wortel',            'Sayuran',        'Kg',     2),
            ('Kecap Manis',       'Bumbu & Rempah', 'Botol', 10),
            ('Saus Sambal',       'Bumbu & Rempah', 'Botol',  5),
            ('Garam',             'Bumbu & Rempah', 'Pack',  10),
            ('Merica Bubuk',      'Bumbu & Rempah', 'Pack',  20),
            ('Teh Celup',         'Minuman',        'Dus',   10),
            ('Kopi Bubuk',        'Minuman',        'Kg',     5),
            ('Es Batu',           'Minuman',        'Karung', 5),
            ('Sabun Cuci Piring', 'Alat Kebersihan','Liter',  5),
            ('Spons Cuci',        'Alat Kebersihan','Pcs',   10),
            ('Plastik Bungkus',   'Lainnya',        'Pack',  20),
        ]

        brg_created = 0
        for nama, kat_nama, sat_nama, min_stok in barangs_data:
            _, created = Barang.objects.get_or_create(
                nama=nama,
                defaults={
                    'kategori': kat_objs[kat_nama],
                    'satuan': sat_objs[sat_nama],
                    'stok_minimal': min_stok,
                    'stok_saat_ini': 0,
                }
            )
            if created:
                brg_created += 1

        self.stdout.write(f'  Barang  : {brg_created} dibuat, {len(barangs_data) - brg_created} sudah ada.')

        # ── 4. Superuser default ───────────────────────────────────────────
        # Dibuat hanya jika belum ada user manapun, atau jika username belum ada.
        import os
        su_username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        su_email    = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@admin.com')
        su_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')

        if su_password and not User.objects.filter(username=su_username).exists():
            User.objects.create_superuser(
                username=su_username,
                email=su_email,
                password=su_password,
            )
            self.stdout.write(f'  Superuser "{su_username}" dibuat.')
        elif User.objects.filter(username=su_username).exists():
            self.stdout.write(f'  Superuser "{su_username}" sudah ada, dilewati.')

        self.stdout.write(self.style.SUCCESS('✔ Seed selesai! Data awal sudah tersedia.'))
