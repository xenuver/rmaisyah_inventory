# Analisis Source Code Aplikasi Inventaris (Bahan Bab 1 - Bab 4 Skripsi)

Berikut adalah ringkasan komprehensif berdasarkan analisis source code di workspace ini. Anda dapat menggunakan struktur dan poin-poin di bawah ini sebagai pedoman untuk merombak Bab 1 hingga Bab 4 agar selaras dengan implementasi sistem (Bab 5) yang ada saat ini.

---

## 1. Konteks Bab 1 (Pendahuluan & Ruang Lingkup)

**Masalah Utama yang Diselesaikan:**
Aplikasi ini dibangun untuk mengatasi masalah pencatatan dan pelacakan inventaris barang. Berdasarkan kode yang ada, aplikasi secara khusus menyelesaikan masalah:
- **Pencatatan Master Data**: Sentralisasi data Kategori, Satuan, dan Barang.
- **Pelacakan Stok Otomatis**: Menghitung penambahan dan pengurangan stok secara *real-time* tanpa perlu perhitungan manual.
- **Manajemen Kadaluarsa (Expired Date) & FIFO**: Menerapkan metode *First-In First-Out* (FIFO) berbasis batch. Barang yang memiliki tanggal kadaluarsa paling dekat akan dikeluarkan/dikurangi terlebih dahulu secara sistem.
- **Sistem Peringatan Dini (Early Warning System)**: Memberikan peringatan saat stok mencapai batas minimal (Stok Kritis) dan ketika ada barang yang mendekati masa kadaluarsa (7 hari sebelum).

**Batasan Masalah (Scope):**
- **Modul yang Tersedia**: 
  1. **Dashboard**: Ringkasan stok kritis, barang mendekati kadaluarsa, aktivitas terbaru, dan visualisasi chart.
  2. **Inventory (Data Master)**: Pengelolaan Barang (CRUD), Kategori, dan Satuan.
  3. **Transactions**: Pencatatan Barang Masuk (dengan info supplier dan exp date) dan Barang Keluar (dengan alasan pemakaian, rusak, dll).
  4. **Ledger/Laporan**: Riwayat transaksi yang bisa diekspor ke format CSV dan PDF.
- **Fitur yang Tidak Ada (Out of Scope)**:
  - Sistem ini **tidak** menangani manajemen multi-gudang (warehouse).
  - **Tidak** ada modul pengadaan (Purchase Order/PO) atau retur ke supplier yang kompleks. Pemasok hanya dicatat sebagai teks (*string*).
  - **Tidak** terintegrasi dengan Point of Sales (POS) atau modul akuntansi/keuangan (tidak ada pencatatan harga beli/jual secara eksplisit di model).

---

## 2. Konteks Bab 2 (Landasan Teori & Teknologi)

**Teknologi yang Digunakan:**
Berdasarkan file `requirements.txt` dan struktur direktori, sistem ini menggunakan ekosistem berikut:
- **Bahasa Pemrograman**: Python
- **Framework Web Utama**: Django (versi 6.0.5)
- **Database**: PostgreSQL (dikoneksikan via library `psycopg` versi 3)
- **Library Tambahan**: 
  - `xhtml2pdf`: Digunakan untuk menghasilkan laporan/cetak dokumen ke format PDF.
  - `asgiref` & `sqlparse`: *Dependency* bawaan dari Django.
- **Teknologi Frontend Interaktif**: HTMX. Terlihat dari penggunaan `HtmxModalMixin` dan pengiriman sinyal `HX-Request` & `HX-Trigger` (seperti `'reloadTable'`) dari Django ke sisi *client* untuk memunculkan modal form tanpa *refresh* halaman secara penuh.

**Arsitektur Sistem:**
Aplikasi ini menggunakan arsitektur **Monolithic** dengan pola rancangan **MVT (Model-View-Template)**, yang merupakan adaptasi pola MVC dari Django. 
Secara spesifik, sistem berbasis *Server-Side Rendering (SSR)* di mana HTML di-render di backend, namun di- *enhance* menggunakan HTMX untuk memberikan pengalaman pengguna yang mendekati *Single Page Application* (SPA) pada fungsi-fungsi CRUD.

---

## 3. Konteks Bab 3 (Analisis Sistem & Hak Akses)

**Aktor / Pengguna Sistem:**
Berdasarkan implementasi *middleware* autentikasi dan penggunaan `LoginRequiredMixin` pada semua *class-based views* di sistem (seperti `BarangListView`, `DashboardView`), aktor dalam aplikasi ini bersifat tunggal atau **semua user yang terdaftar dianggap memiliki hak akses penuh** (*Admin/Petugas Inventaris*).
- Syarat mutlak: Pengguna wajib melakukan login untuk mengakses semua halaman (`/accounts/login/`).
- Tidak ada pembagian akses (Role-Based Access Control) yang spesifik (seperti Staff vs Manager) di level kode fungsi.

**Alur Kerja Utama (Business Flow):**
1. **Pendataan Awal**: Pengguna harus mengisi Master Data yaitu "Kategori" dan "Satuan". Setelah itu, pengguna bisa mendaftarkan "Barang". Jika barang baru didaftarkan dengan nilai stok awal > 0, sistem otomatis membuatkan record Transaksi Barang Masuk pertama (Stok Awal).
2. **Alur Barang Masuk**: Pengguna mengisi formulir Barang Masuk (jumlah, supplier, dan masa kadaluarsa jika ada). Sistem akan menambah `stok_saat_ini` di master Barang dan membuat sebuah *Batch* baru (melalui model `StokBatch`) untuk melacak kelompok stok tersebut.
3. **Alur Barang Keluar**: Pengguna menginput barang keluar beserta alasannya (Pemakaian Dapur, Rusak, Kadaluarsa, Lainnya). Sistem melakukan **Validasi Stok** (mencegah simpan jika stok kurang). Selanjutnya sistem menerapkan **Logika FIFO**: Mencari batch barang dengan tanggal kadaluarsa paling awal, memotong stok pada batch tersebut. Jika satu batch habis, pemotongan dilanjutkan ke batch berikutnya.
4. **Alur Laporan (Ledger)**: Semua transaksi masuk dan keluar digabung dan diurutkan secara kronologis untuk menampilkan buku besar (Ledger), yang kemudian bisa difilter berdasarkan tanggal dan diekspor oleh pengguna.

---

## 4. Konteks Bab 4 (Implementasi & Antarmuka)

**Daftar Halaman Utama (Views/UI):**
Aplikasi berhasil merender sejumlah antarmuka (berdasarkan struktur di folder `templates` dan `views.py`):
1. **Halaman Dashboard**: Menampilkan ringkasan matriks stok kritis, notifikasi mendekati kadaluarsa, aktivitas terkini, *chart doughnut* kategori, dan *line chart* tren barang masuk/keluar.
2. **Halaman Master Inventory**:
   - Daftar Barang (serta modal form Tambah/Edit/Hapus).
   - Daftar Kategori (serta modal form Tambah/Edit/Hapus).
   - Daftar Satuan (serta modal form Tambah/Edit/Hapus).
3. **Halaman Transaksi**:
   - Daftar Log Barang Masuk (serta modal Catat Masuk).
   - Daftar Log Barang Keluar (serta modal Catat Keluar).
4. **Halaman Buku Besar (Ledger)**: Halaman rekapitulasi transaksi masuk dan keluar dengan kemampuan filter (tanggal, tipe transaksi) dan tombol Export CSV serta Export PDF.

**Pengujian Sistem (Testing):**
Dalam *codebase* ini, **tidak ditemukan** pengujian otomatis (*Unit Testing* atau *Integration Testing* yang menggunakan modul `unittest` atau `pytest` dari Django). Oleh karena itu, pengujian harus diceritakan sebagai **Pengujian Manual (Black Box Testing)**.

**Fungsi Krusial yang Wajib Diuji Secara Manual (Sertakan sebagai skenario uji di Bab 4):**
1. **Pengujian Logika FIFO (Kadaluarsa)**: Lakukan uji coba input Barang Masuk dengan 2 batch tanggal expired berbeda. Coba keluarkan barang, dan pastikan sistem memotong stok dari batch dengan *expired date* tercepat (awal) lebih dulu.
2. **Pengujian Validasi Stok Kurang**: Lakukan uji coba input Barang Keluar melebihi sisa `stok_saat_ini`. Sistem harus memblokir form dan memunculkan *error message* `ValidationError` (Stok tidak mencukupi).
3. **Pengujian Proteksi Data Master (*Foreign Key Constraint*)**: Cobalah menghapus "Kategori" atau "Satuan" yang sedang dipakai oleh sebuah "Barang". Pastikan muncul pesan *error* ("Tidak dapat menghapus... terikat transaksi") berkat proteksi `ProtectedError` dari database, dan aplikasi tidak *crash*.
4. **Pengujian Reaktivitas HTMX**: Uji coba penambahan/edit data dari Modal Form, lalu pastikan tabel di belakangnya otomatis ter-*update*/*reload* (tanpa memuat ulang seluruh halaman web).
5. **Pengujian Export Data**: Pastikan dokumen PDF yang dihasilkan tidak terpotong tabelnya dan ekspor CSV dapat dibaca di Excel dengan kolom yang terpisah rapi.
