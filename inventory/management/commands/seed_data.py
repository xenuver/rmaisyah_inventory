from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta, date

from inventory.models import Kategori, Satuan, Barang
from transactions.models import BarangMasuk, BarangKeluar

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
            help='Lewati seeding jika data sudah ada di database.',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Hapus semua data lama lalu seed ulang dari awal (BERBAHAYA di production!).',
        )

    def handle(self, *args, **kwargs):
        skip_if_exists = kwargs.get('skip_if_exists', False)
        force = kwargs.get('force', False)

        if force:
            self.stdout.write(self.style.WARNING('--force aktif: Menghapus semua data lama...'))
            from transactions.models import BarangKeluarBatch, StokBatch
            BarangKeluarBatch.objects.all().delete()
            StokBatch.objects.all().delete()
            BarangMasuk.objects.all().delete()
            BarangKeluar.objects.all().delete()
            Barang.objects.all().delete()
            Kategori.objects.all().delete()
            Satuan.objects.all().delete()
            User.objects.filter(is_superuser=True).delete()
            self.stdout.write('Data lama dihapus. Mulai seeding...')

        # ── 1. Kategori ────────────────────────────────────────────────────
        kategoris_data = [
            ('Bahan Pokok',     'Kategori untuk bahan pokok'),
            ('Sayuran',         'Kategori untuk sayuran'),
            ('Bumbu & Rempah',  'Kategori untuk bumbu & rempah'),
            ('Daging & Ikan',   'Kategori untuk daging & ikan'),
            ('Minuman',         'Kategori untuk minuman'),
            ('Alat Kebersihan', 'Kategori untuk alat kebersihan'),
            ('Lainnya',         'Kategori untuk lainnya'),
        ]
        kat_objs = {}
        kat_created = 0
        for nama, deskripsi in kategoris_data:
            obj, created = Kategori.objects.get_or_create(
                nama=nama, defaults={'deskripsi': deskripsi}
            )
            kat_objs[nama] = obj
            if created:
                kat_created += 1
        self.stdout.write(f'  Kategori : {kat_created} dibuat, {len(kategoris_data) - kat_created} sudah ada.')

        # ── 2. Satuan ──────────────────────────────────────────────────────
        satuans_data = ['Kg', 'Liter', 'Pcs', 'Ikat', 'Gram', 'Dus', 'Botol', 'Karung', 'Pack']
        sat_objs = {}
        sat_created = 0
        for nama in satuans_data:
            obj, created = Satuan.objects.get_or_create(nama=nama)
            sat_objs[nama] = obj
            if created:
                sat_created += 1
        self.stdout.write(f'  Satuan   : {sat_created} dibuat, {len(satuans_data) - sat_created} sudah ada.')

        # ── 3. Barang ──────────────────────────────────────────────────────
        # Format: (nama, kategori, satuan, stok_minimal)
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

        brg_objs = {}
        brg_created = 0
        for nama, kat_nama, sat_nama, min_stok in barangs_data:
            obj, created = Barang.objects.get_or_create(
                nama=nama,
                defaults={
                    'kategori': kat_objs[kat_nama],
                    'satuan':   sat_objs[sat_nama],
                    'stok_minimal': min_stok,
                    'stok_saat_ini': 0,
                }
            )
            brg_objs[nama] = obj
            if created:
                brg_created += 1
        self.stdout.write(f'  Barang   : {brg_created} dibuat, {len(barangs_data) - brg_created} sudah ada.')

        # ── 4. Transaksi Barang Masuk & Keluar ────────────────────────────
        # Lewati jika sudah ada transaksi (idempotent)
        if BarangMasuk.objects.exists():
            self.stdout.write(self.style.WARNING(
                '  Transaksi sudah ada — seeding transaksi dilewati.'
            ))
        else:
            self._seed_transaksi(brg_objs)

        # ── 5. Superuser ───────────────────────────────────────────────────
        import os
        su_username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        su_email    = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@admin.com')
        su_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

        if su_password and not User.objects.filter(username=su_username).exists():
            User.objects.create_superuser(
                username=su_username, email=su_email, password=su_password,
            )
            self.stdout.write(f'  Superuser "{su_username}" dibuat.')
        else:
            self.stdout.write(f'  Superuser "{su_username}" sudah ada, dilewati.')

        self.stdout.write(self.style.SUCCESS('[OK] Seed selesai! Data awal sudah tersedia.'))

    # ──────────────────────────────────────────────────────────────────────────
    def _seed_transaksi(self, brg_objs):
        """
        Buat transaksi masuk & keluar secara kronologis selama 30 hari terakhir.
        Data deterministik (bukan random) agar konsisten setiap deploy.
        """
        today = timezone.now().date()

        suppliers = [
            'PT. Pangan Makmur',
            'Toko Sembako Abadi',
            'Pasar Tradisional Induk',
            'Agen Telur Berkah',
            'CV. Sumber Rezeki',
        ]

        # ── Jadwal Barang Masuk ────────────────────────────────────────
        # Format: (nama_barang, hari_lalu, jumlah, supplier_idx, keterangan, hari_exp)
        # hari_exp=None berarti tanpa kadaluarsa
        masuk_schedule = [
            # Bahan Pokok — restock mingguan
            ('Beras Premium',     29, 100, 0, 'Restock bulanan beras premium',    90),
            ('Beras Biasa',       28, 150, 1, 'Restock bulanan beras biasa',       90),
            ('Minyak Goreng',     27,  50, 2, 'Pembelian minyak goreng',           180),
            ('Tepung Terigu',     26,  80, 0, 'Restock tepung terigu',             180),
            ('Gula Pasir',        25, 100, 1, 'Pembelian gula pasir bulanan',      365),
            ('Beras Premium',     14,  80, 0, 'Restock pertengahan bulan',         90),
            ('Beras Biasa',       13, 100, 1, 'Restock pertengahan bulan',         90),
            ('Minyak Goreng',     12,  40, 2, 'Tambahan minyak goreng',            180),

            # Daging & Ikan — restock 2x seminggu
            ('Ayam Potong',       29,  50, 3, 'Pasokan ayam mingguan',            7),
            ('Ayam Potong',       22,  50, 3, 'Pasokan ayam mingguan',            7),
            ('Ayam Potong',       15,  50, 3, 'Pasokan ayam mingguan',            7),
            ('Ayam Potong',        8,  50, 3, 'Pasokan ayam mingguan',            7),
            ('Ayam Potong',        1,  50, 3, 'Pasokan ayam mingguan',            7),
            ('Daging Sapi',       28,  30, 2, 'Pasokan daging sapi',              5),
            ('Daging Sapi',       21,  30, 2, 'Pasokan daging sapi',              5),
            ('Daging Sapi',       14,  30, 2, 'Pasokan daging sapi',              5),
            ('Daging Sapi',        7,  30, 2, 'Pasokan daging sapi',              5),
            ('Telur Ayam',        27,  60, 3, 'Pembelian telur ayam',             14),
            ('Telur Ayam',        20,  60, 3, 'Pembelian telur ayam',             14),
            ('Telur Ayam',        13,  60, 3, 'Pembelian telur ayam',             14),
            ('Telur Ayam',         6,  60, 3, 'Pembelian telur ayam',             14),
            ('Ikan Nila',         26,  40, 4, 'Pasokan ikan nila segar',          3),
            ('Ikan Nila',         19,  40, 4, 'Pasokan ikan nila segar',          3),
            ('Ikan Nila',         12,  40, 4, 'Pasokan ikan nila segar',          3),
            ('Ikan Nila',          5,  40, 4, 'Pasokan ikan nila segar',          3),

            # Sayuran & Bumbu — restock mingguan
            ('Bawang Merah',      25,  30, 2, 'Pembelian bumbu dapur',            14),
            ('Bawang Merah',      18,  30, 2, 'Pembelian bumbu dapur',            14),
            ('Bawang Merah',      11,  30, 2, 'Pembelian bumbu dapur',            14),
            ('Bawang Putih',      24,  25, 2, 'Pembelian bumbu dapur',            30),
            ('Bawang Putih',      17,  25, 2, 'Pembelian bumbu dapur',            30),
            ('Bawang Putih',      10,  25, 2, 'Pembelian bumbu dapur',            30),
            ('Cabai Merah',       23,  20, 4, 'Pembelian cabai segar',            7),
            ('Cabai Merah',       16,  20, 4, 'Pembelian cabai segar',            7),
            ('Cabai Merah',        9,  20, 4, 'Pembelian cabai segar',            7),
            ('Cabai Merah',        2,  20, 4, 'Pembelian cabai segar',            7),
            ('Cabai Rawit',       22,  15, 4, 'Pembelian cabai rawit',            7),
            ('Cabai Rawit',       15,  15, 4, 'Pembelian cabai rawit',            7),
            ('Cabai Rawit',        8,  15, 4, 'Pembelian cabai rawit',            7),
            ('Tomat',             21,  25, 4, 'Pembelian tomat segar',            5),
            ('Tomat',             14,  25, 4, 'Pembelian tomat segar',            5),
            ('Tomat',              7,  25, 4, 'Pembelian tomat segar',            5),
            ('Wortel',            20,  30, 1, 'Pembelian wortel',                 14),
            ('Wortel',            13,  30, 1, 'Pembelian wortel',                 14),
            ('Wortel',             6,  30, 1, 'Pembelian wortel',                 14),

            # Bumbu kemasan
            ('Kecap Manis',       29,  24, 0, 'Restock kecap manis (1 dus)',      365),
            ('Kecap Manis',       15,  24, 0, 'Restock kecap manis (1 dus)',      365),
            ('Saus Sambal',       28,  12, 0, 'Restock saus sambal',              365),
            ('Saus Sambal',       14,  12, 0, 'Restock saus sambal',              365),
            ('Garam',             27,  50, 1, 'Pembelian garam dapur',            None),
            ('Merica Bubuk',      26,  30, 1, 'Pembelian merica bubuk',           365),

            # Minuman & Lainnya
            ('Teh Celup',         25,  20, 0, 'Restock teh celup',               365),
            ('Kopi Bubuk',        24,  15, 0, 'Restock kopi bubuk',              365),
            ('Es Batu',           29,  20, 4, 'Pasokan es batu mingguan',        None),
            ('Es Batu',           22,  20, 4, 'Pasokan es batu mingguan',        None),
            ('Es Batu',           15,  20, 4, 'Pasokan es batu mingguan',        None),
            ('Es Batu',            8,  20, 4, 'Pasokan es batu mingguan',        None),
            ('Es Batu',            1,  20, 4, 'Pasokan es batu mingguan',        None),

            # Alat Kebersihan
            ('Sabun Cuci Piring', 28,  10, 0, 'Restock sabun cuci piring',       None),
            ('Spons Cuci',        28,  20, 0, 'Restock spons cuci',              None),
            ('Plastik Bungkus',   27,  30, 0, 'Restock plastik bungkus',         None),
        ]

        # Urutkan dari paling lama ke terbaru (hari_lalu besar duluan)
        masuk_schedule.sort(key=lambda x: x[1], reverse=True)

        masuk_count = 0
        for nama, hari_lalu, jumlah, sup_idx, ket, exp_days in masuk_schedule:
            barang = brg_objs.get(nama)
            if not barang:
                continue
            tgl = today - timedelta(days=hari_lalu)
            exp = (tgl + timedelta(days=exp_days)) if exp_days else None
            bm = BarangMasuk.objects.create(
                barang=barang,
                jumlah=jumlah,
                supplier=suppliers[sup_idx],
                tanggal=tgl,
                tanggal_kadaluarsa=exp,
                keterangan=ket,
            )
            # Backdate created_at agar urutan log rapi
            BarangMasuk.objects.filter(pk=bm.pk).update(
                created_at=timezone.make_aware(
                    timezone.datetime.combine(tgl, timezone.datetime.min.time())
                    + timedelta(hours=8)
                )
            )
            masuk_count += 1

        self.stdout.write(f'  Masuk    : {masuk_count} transaksi barang masuk dibuat.')

        # ── Jadwal Barang Keluar ───────────────────────────────────────
        # Format: (nama_barang, hari_lalu, jumlah, alasan, keterangan)
        keluar_schedule = [
            # Pemakaian harian beras (setiap hari ±10 kg)
            ('Beras Premium',  28, 8,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Beras Premium',  27, 10, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Beras Premium',  26, 9,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Beras Premium',  25, 11, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Beras Premium',  24, 10, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Beras Premium',  23, 9,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Beras Premium',  20, 10, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Beras Premium',  15, 10, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Beras Premium',  10, 12, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Beras Premium',   5, 10, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Beras Biasa',    27, 15, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Beras Biasa',    25, 12, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Beras Biasa',    20, 18, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Beras Biasa',    15, 14, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Beras Biasa',    10, 16, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Beras Biasa',     5, 15, 'pemakaian_dapur', 'Pemakaian dapur harian'),

            # Minyak Goreng
            ('Minyak Goreng',  27, 5,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Minyak Goreng',  24, 6,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Minyak Goreng',  20, 5,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Minyak Goreng',  15, 7,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Minyak Goreng',  10, 5,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Minyak Goreng',   5, 6,  'pemakaian_dapur', 'Pemakaian dapur harian'),

            # Ayam Potong — pemakaian harian besar
            ('Ayam Potong',    28, 8,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Ayam Potong',    27, 10, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Ayam Potong',    26, 9,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Ayam Potong',    25, 12, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Ayam Potong',    24, 10, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Ayam Potong',    21, 11, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Ayam Potong',    20, 9,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Ayam Potong',    15, 10, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Ayam Potong',    14, 8,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Ayam Potong',    10, 12, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Ayam Potong',     7, 10, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Ayam Potong',     5, 9,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Ayam Potong',     3, 10, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Ayam Potong',     1, 8,  'pemakaian_dapur', 'Pemakaian dapur harian'),

            # Daging Sapi
            ('Daging Sapi',    27, 5,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Daging Sapi',    24, 6,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Daging Sapi',    20, 5,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Daging Sapi',    13, 6,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Daging Sapi',    10, 5,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Daging Sapi',     6, 6,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Daging Sapi',     3, 4,  'pemakaian_dapur', 'Pemakaian dapur harian'),

            # Telur Ayam
            ('Telur Ayam',     26, 8,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Telur Ayam',     22, 10, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Telur Ayam',     19, 8,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Telur Ayam',     12, 9,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Telur Ayam',      5, 10, 'pemakaian_dapur', 'Pemakaian dapur harian'),

            # Ikan Nila
            ('Ikan Nila',      25, 8,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Ikan Nila',      18, 10, 'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Ikan Nila',      11, 8,  'pemakaian_dapur', 'Pemakaian dapur harian'),
            ('Ikan Nila',       4, 9,  'pemakaian_dapur', 'Pemakaian dapur harian'),

            # Sayuran & Bumbu
            ('Bawang Merah',   24, 4,  'pemakaian_dapur', 'Pemakaian bumbu harian'),
            ('Bawang Merah',   17, 5,  'pemakaian_dapur', 'Pemakaian bumbu harian'),
            ('Bawang Merah',   10, 4,  'pemakaian_dapur', 'Pemakaian bumbu harian'),
            ('Bawang Merah',    3, 5,  'pemakaian_dapur', 'Pemakaian bumbu harian'),
            ('Bawang Putih',   23, 3,  'pemakaian_dapur', 'Pemakaian bumbu harian'),
            ('Bawang Putih',   16, 4,  'pemakaian_dapur', 'Pemakaian bumbu harian'),
            ('Bawang Putih',    9, 3,  'pemakaian_dapur', 'Pemakaian bumbu harian'),
            ('Bawang Putih',    2, 4,  'pemakaian_dapur', 'Pemakaian bumbu harian'),
            ('Cabai Merah',    22, 3,  'pemakaian_dapur', 'Pemakaian cabai harian'),
            ('Cabai Merah',    15, 4,  'pemakaian_dapur', 'Pemakaian cabai harian'),
            ('Cabai Merah',     8, 3,  'pemakaian_dapur', 'Pemakaian cabai harian'),
            ('Cabai Merah',     1, 4,  'pemakaian_dapur', 'Pemakaian cabai harian'),
            ('Cabai Rawit',    21, 2,  'pemakaian_dapur', 'Pemakaian cabai rawit harian'),
            ('Cabai Rawit',    14, 3,  'pemakaian_dapur', 'Pemakaian cabai rawit harian'),
            ('Cabai Rawit',     7, 2,  'pemakaian_dapur', 'Pemakaian cabai rawit harian'),
            ('Tomat',          20, 5,  'pemakaian_dapur', 'Pemakaian tomat harian'),
            ('Tomat',          13, 5,  'pemakaian_dapur', 'Pemakaian tomat harian'),
            ('Tomat',           6, 5,  'pemakaian_dapur', 'Pemakaian tomat harian'),
            ('Wortel',         19, 4,  'pemakaian_dapur', 'Pemakaian wortel harian'),
            ('Wortel',         12, 5,  'pemakaian_dapur', 'Pemakaian wortel harian'),
            ('Wortel',          5, 4,  'pemakaian_dapur', 'Pemakaian wortel harian'),

            # Bumbu kemasan
            ('Kecap Manis',    28, 3,  'pemakaian_dapur', 'Pemakaian kecap harian'),
            ('Kecap Manis',    14, 3,  'pemakaian_dapur', 'Pemakaian kecap harian'),
            ('Saus Sambal',    27, 2,  'pemakaian_dapur', 'Pemakaian saus harian'),
            ('Saus Sambal',    13, 2,  'pemakaian_dapur', 'Pemakaian saus harian'),
            ('Garam',          26, 5,  'pemakaian_dapur', 'Pemakaian garam harian'),
            ('Garam',          10, 5,  'pemakaian_dapur', 'Pemakaian garam harian'),
            ('Merica Bubuk',   25, 3,  'pemakaian_dapur', 'Pemakaian merica harian'),
            ('Merica Bubuk',   10, 3,  'pemakaian_dapur', 'Pemakaian merica harian'),

            # Minuman
            ('Teh Celup',      24, 2,  'pemakaian_dapur', 'Pemakaian teh harian'),
            ('Kopi Bubuk',     23, 2,  'pemakaian_dapur', 'Pemakaian kopi harian'),
            ('Es Batu',        28, 3,  'pemakaian_dapur', 'Pemakaian es batu harian'),
            ('Es Batu',        21, 4,  'pemakaian_dapur', 'Pemakaian es batu harian'),
            ('Es Batu',        14, 3,  'pemakaian_dapur', 'Pemakaian es batu harian'),
            ('Es Batu',         7, 4,  'pemakaian_dapur', 'Pemakaian es batu harian'),

            # Kerusakan
            ('Ikan Nila',      18, 2,  'rusak',           'Ikan tidak segar, dibuang'),
            ('Tomat',          13, 3,  'rusak',           'Tomat busuk, dibuang'),
            ('Cabai Merah',     9, 2,  'rusak',           'Cabai layu, dibuang'),

            # Alat kebersihan
            ('Sabun Cuci Piring', 27, 2, 'pemakaian_dapur', 'Pemakaian sabun cuci dapur'),
            ('Sabun Cuci Piring', 14, 2, 'pemakaian_dapur', 'Pemakaian sabun cuci dapur'),
            ('Spons Cuci',        26, 3, 'pemakaian_dapur', 'Pemakaian spons cuci'),
            ('Plastik Bungkus',   25, 5, 'pemakaian_dapur', 'Pemakaian plastik bungkus'),
            ('Plastik Bungkus',   10, 5, 'pemakaian_dapur', 'Pemakaian plastik bungkus'),
        ]

        # Urutkan dari paling lama ke terbaru — penting untuk validasi stok FIFO
        keluar_schedule.sort(key=lambda x: x[1], reverse=True)

        keluar_count = 0
        keluar_skip = 0
        for nama, hari_lalu, jumlah, alasan, ket in keluar_schedule:
            barang = brg_objs.get(nama)
            if not barang:
                continue
            # Refresh stok terkini
            barang.refresh_from_db()
            if barang.stok_saat_ini < jumlah:
                keluar_skip += 1
                continue  # Stok tidak cukup, lewati
            tgl = today - timedelta(days=hari_lalu)
            bk = BarangKeluar.objects.create(
                barang=barang,
                jumlah=jumlah,
                alasan=alasan,
                tanggal=tgl,
                keterangan=ket,
            )
            BarangKeluar.objects.filter(pk=bk.pk).update(
                created_at=timezone.make_aware(
                    timezone.datetime.combine(tgl, timezone.datetime.min.time())
                    + timedelta(hours=14)
                )
            )
            keluar_count += 1

        self.stdout.write(
            f'  Keluar   : {keluar_count} transaksi barang keluar dibuat'
            + (f' ({keluar_skip} dilewati karena stok tidak cukup).' if keluar_skip else '.')
        )
