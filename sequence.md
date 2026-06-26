# Sequence Diagram - Sistem Informasi Persediaan Rumah Makan Aisyah Ngabang

Dokumen ini berisi Sequence Diagram (*Diagram Urutan*) yang dirancang khusus untuk mempermudah *programmer* memahami alur pertukaran data (terutama interaksi HTMX, logika *database transaction*, dan algoritma FIFO). Gunakan [plantuml.com/plantuml](https://www.plantuml.com/plantuml) atau ekstensi PlantUML untuk merendernya.

---

## 1. Alur Login Sistem
Menjelaskan bagaimana pengguna melakukan otentikasi (login) untuk masuk ke dalam aplikasi menggunakan verifikasi data dan pembuatan *session*.

```plantuml
@startuml
autonumber
actor Pengguna as U
participant Browser as B
participant "Login View" as V
participant "Django Auth" as A
participant Database as DB

U -> B: Membuka Halaman Login (/login)
B -> V: GET /login
V --> B: Render Halaman Form Login
B --> U: Tampilkan Form Login

U -> B: Memasukkan username & password
B -> V: POST /login
V -> A: authenticate(username, password)
A -> DB: Verifikasi kredensial
DB --> A: Return User object (jika valid)

alt Kredensial Tidak Valid
    A --> V: Return None
    V --> B: Tampilkan Pesan Error
    B --> U: Tampilkan notifikasi "Login Gagal"
else Kredensial Valid
    A --> V: Return User
    V -> A: login(request, user)
    note right of A
        Membuat dan menyimpan
        session_id untuk akses lanjut
    end note
    A --> V: Session Created
    V --> B: Redirect ke /dashboard
    B --> U: Tampilkan Halaman Dashboard
end
@enduml
```

---

## 2. Alur Kelola Data Barang
Menjelaskan bagaimana sistem memproses operasi CRUD (Create, Read, Update, Delete) pada entitas Barang menggunakan modal HTMX tanpa me-*refresh* seluruh halaman.

```plantuml
@startuml
autonumber
actor Pengguna as U
participant "Browser (HTMX)" as B
participant "Barang View" as V
participant "Barang Form" as F
participant "Barang Model" as M

U -> B: Klik tombol Tambah/Edit
B -> V: GET request (via HTMX)
V -> F: Inisialisasi Form kosong / terisi data lama
V --> B: Render HTML Modal Form
B --> U: Tampilkan Modal Pop-up

U -> B: Isi form & Submit
B -> V: POST request (via HTMX)
V -> F: Validasi Data Form

alt Data Tidak Valid
    F --> V: Return ValidationError
    V --> B: Render ulang HTML Modal + Pesan Error
    B --> U: Tampilkan error di dalam Modal
else Data Valid
    F -> M: save()
    M --> F: Data berhasil tersimpan
    note right of V: Menambahkan Header khusus untuk HTMX
    V --> B: HTTP 204 No Content\n(Header: HX-Trigger='reloadTable')
    B -> B: Modal ditutup otomatis
    
    note right of B: Menangkap event 'reloadTable'
    B -> V: GET request tabel terbaru (HTMX)
    V --> B: HTML Tabel Baru
    B --> U: Tabel ter-update tanpa full-refresh
end
@enduml
```

---

## 3. Alur Kelola Kategori
Menjelaskan bagaimana sistem memproses operasi CRUD (Create, Read, Update, Delete) pada entitas Kategori menggunakan modal HTMX tanpa me-*refresh* seluruh halaman.

```plantuml
@startuml
autonumber
actor Pengguna as U
participant "Browser (HTMX)" as B
participant "Kategori View" as V
participant "Kategori Form" as F
participant "Kategori Model" as M

U -> B: Klik tombol Tambah/Edit
B -> V: GET request (via HTMX)
V -> F: Inisialisasi Form kosong / terisi data lama
V --> B: Render HTML Modal Form
B --> U: Tampilkan Modal Pop-up

U -> B: Isi form & Submit
B -> V: POST request (via HTMX)
V -> F: Validasi Data Form

alt Data Tidak Valid
    F --> V: Return ValidationError
    V --> B: Render ulang HTML Modal + Pesan Error
    B --> U: Tampilkan error di dalam Modal
else Data Valid
    F -> M: save()
    M --> F: Data berhasil tersimpan
    note right of V: Menambahkan Header khusus untuk HTMX
    V --> B: HTTP 204 No Content\n(Header: HX-Trigger='reloadTable')
    B -> B: Modal ditutup otomatis
    
    note right of B: Menangkap event 'reloadTable'
    B -> V: GET request tabel terbaru (HTMX)
    V --> B: HTML Tabel Baru
    B --> U: Tabel ter-update tanpa full-refresh
end
@enduml
```

---

## 4. Alur Kelola Satuan
Menjelaskan bagaimana sistem memproses operasi CRUD (Create, Read, Update, Delete) pada entitas Satuan menggunakan modal HTMX tanpa me-*refresh* seluruh halaman.

```plantuml
@startuml
autonumber
actor Pengguna as U
participant "Browser (HTMX)" as B
participant "Satuan View" as V
participant "Satuan Form" as F
participant "Satuan Model" as M

U -> B: Klik tombol Tambah/Edit
B -> V: GET request (via HTMX)
V -> F: Inisialisasi Form kosong / terisi data lama
V --> B: Render HTML Modal Form
B --> U: Tampilkan Modal Pop-up

U -> B: Isi form & Submit
B -> V: POST request (via HTMX)
V -> F: Validasi Data Form

alt Data Tidak Valid
    F --> V: Return ValidationError
    V --> B: Render ulang HTML Modal + Pesan Error
    B --> U: Tampilkan error di dalam Modal
else Data Valid
    F -> M: save()
    M --> F: Data berhasil tersimpan
    note right of V: Menambahkan Header khusus untuk HTMX
    V --> B: HTTP 204 No Content\n(Header: HX-Trigger='reloadTable')
    B -> B: Modal ditutup otomatis
    
    note right of B: Menangkap event 'reloadTable'
    B -> V: GET request tabel terbaru (HTMX)
    V --> B: HTML Tabel Baru
    B --> U: Tabel ter-update tanpa full-refresh
end
@enduml
```

---

## 5. Alur Pencatatan Barang Masuk
Menjelaskan proses saat pengguna mencatat stok masuk. Sistem harus mencatat transaksi riwayat dan membuat `StokBatch` baru yang akan digunakan untuk FIFO.

```plantuml
@startuml
autonumber
actor Pengguna as U
participant "BarangMasuk View" as V
participant "BarangMasuk Model" as M
participant "StokBatch Model" as S
participant "Barang Model" as B
participant Database as DB

U -> V: Submit Form Barang Masuk (HTMX POST)
V -> M: Validasi Form & panggil save()

group transaction.atomic()
    M -> DB: INSERT data ke tabel BarangMasuk
    
    M -> S: Buat StokBatch baru
    note right of S
        Menyimpan jumlah awal, jumlah sekarang,
        dan tanggal kadaluarsa dari transaksi.
    end note
    S -> DB: INSERT data ke tabel StokBatch
    
    M -> B: Ambil objek Barang terkait
    B -> B: stok_saat_ini += jumlah_masuk
    B -> DB: UPDATE tabel Barang
end

V --> U: Sukses & HTMX Reload Tabel
@enduml
```

---

## 6. Alur Pencatatan Barang Keluar (Algoritma FIFO)
Menjelaskan logika *First-In First-Out* (FIFO) yang sangat penting di sistem ini. Pengeluaran memprioritaskan batch yang paling dekat dengan tanggal kedaluwarsa atau yang dicatat paling awal.

```plantuml
@startuml
autonumber
actor Pengguna as U
participant "BarangKeluar View" as V
participant "BarangKeluar Model" as BK
participant "StokBatch Model" as SB
participant "BarangKeluarBatch Model" as BKB
participant "Barang Model" as B

U -> V: Submit Form Barang Keluar (jumlah: X)
V -> BK: Validasi Form & panggil save()

group transaction.atomic()
    BK -> B: Cek (stok_saat_ini >= jumlah_keluar)
    alt Stok Tidak Cukup
        B --> BK: Raise ValidationError
        BK --> V: Gagalkan proses penyimpanan
        V --> U: Tampilkan pesan "Stok tidak mencukupi"
    else Stok Cukup
        note right of BK: Terapkan Logika FIFO
        BK -> SB: select_for_update().filter(jumlah_sekarang > 0)
        note right of SB
            ORDER BY tanggal_kadaluarsa ASC,
            created_at ASC
        end note
        SB --> BK: Mengembalikan QuerySet Batch aktif
        
        loop Iterasi Batch hingga sisa pengeluaran = 0
            BK -> SB: Kurangi 'jumlah_sekarang' pada Batch terkait
            SB -> SB: save() (UPDATE Database)
            
            BK -> BKB: create(barang_keluar, stok_batch, jumlah_dipotong)
            note right of BKB
                Simpan riwayat pemotongan (BarangKeluarBatch)
                untuk pelacakan stok.
            end note
        end
        
        BK -> B: stok_saat_ini -= jumlah_keluar
        B -> B: save() (UPDATE Database)
        
        BK -> BK: Simpan data transaksi BarangKeluar ke Database
    end
end

V --> U: Sukses & HTMX Reload Tabel
@enduml
```

---

## 7. Alur Memuat Dashboard (Pemrosesan Grafik & Analitik)
Menjelaskan interaksi antara *View* yang menyiapkan struktur JSON dan Javascript (*Chart.js*) di sisi klien yang merendernya.

```plantuml
@startuml
autonumber
actor Pengguna as U
participant Browser as B
participant "Dashboard View" as V
participant Database as DB
participant "Chart.js (Frontend)" as C

U -> B: Akses Halaman Utama (/dashboard)
B -> V: GET /dashboard

V -> DB: Query Barang dengan stok_saat_ini <= stok_minimal
DB --> V: Return list Stok Kritis

V -> DB: Query StokBatch yang mendekati kadaluarsa
DB --> V: Return list Bahan Mendekati Kadaluarsa

V -> DB: Agregasi Distribusi Kategori & Tren Transaksi Bulanan
DB --> V: Return Raw Data Agregasi

note right of V: Konversi Raw Data agregasi menjadi string JSON
V --> B: Return HTML (menyisipkan JSON ke dalam script context)

B -> C: Browser mengeksekusi Javascript
note right of C: Chart.js membaca JSON dari HTML DOM
C -> C: Render Pie Chart & Bar/Line Chart
C --> U: Grafik tampil di layar Pengguna
@enduml
```

---

## 8. Alur Melihat Laporan Buku Besar
Menjelaskan proses saat pengguna mengakses halaman Buku Besar, di mana sistem menarik log aktivitas masuk dan keluar, menggabungkannya, dan mengurutkannya secara kronologis berdasarkan filter tanggal.

```plantuml
@startuml
autonumber
actor Pengguna as U
participant Browser as B
participant "Buku Besar View" as V
participant Database as DB

U -> B: Mengakses Halaman Buku Besar
B -> V: GET /buku-besar (dengan param filter opsional)

V -> DB: Query data BarangMasuk (sesuai filter)
DB --> V: Return QuerySet BarangMasuk
V -> DB: Query data BarangKeluar (sesuai filter)
DB --> V: Return QuerySet BarangKeluar

note right of V
  Menggabungkan kedua QuerySet
  dan mengurutkan secara kronologis
  (berdasarkan tanggal/waktu).
end note
V -> V: Merge & Sort Transaksi

V --> B: Render HTML Tabel Buku Besar
B --> U: Tampilkan Tabel Riwayat Transaksi Lengkap
@enduml
```

---

## 9. Alur Unduh/Ekspor Laporan
Menjelaskan bagaimana sistem memproses hasil filter pada Buku Besar dan menghasilkan file berkas (CSV / PDF) yang kemudian diunduh (*download*) oleh pengguna.

```plantuml
@startuml
autonumber
actor Pengguna as U
participant Browser as B
participant "Buku Besar View" as V
participant Database as DB
participant "Export Service" as E

U -> B: Mengklik tombol Export (CSV/PDF) pada filter
B -> V: GET /buku-besar/export?start_date=X&end_date=Y&format=Z
V -> DB: Query data transaksi masuk & keluar sesuai filter
DB --> V: Return QuerySet Data Transaksi

V -> E: Panggil fungsi Export sesuai format
alt Format CSV
    E -> E: Tulis baris per baris menggunakan modul csv
    E --> V: Return HttpResponse (Content-Type: text/csv)
else Format PDF
    E -> E: Render Template HTML menjadi PDF
    E --> V: Return HttpResponse (Content-Type: application/pdf)
end

note right of V
    Menambahkan Header: 
    Content-Disposition=attachment; filename=...
end note
V --> B: Kirim file (unduhan)
B --> U: Browser mendownload dan menyimpan ke Perangkat
@enduml
```
