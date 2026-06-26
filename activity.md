# Activity Diagram - Sistem Informasi Persediaan Rumah Makan Aisyah Ngabang

Paste setiap blok kode ke [mermaid.live](https://mermaid.live/) atau gunakan ekstensi Markdown untuk render diagram.

---

## 1. Activity Diagram Login

```mermaid
flowchart TD
    subgraph Pengguna
        P_Start((Start)) --> P1[Mengakses sistem melalui peramban]
        P1 --> P2[Memasukkan nama pengguna dan kata sandi]
        P2 --> P3[Menekan tombol Login]
        P4[Mengakses Dashboard] --> P_Stop1((Stop))
        P5[Mengulang pengisian kredensial] --> P_Stop2((Stop))
    end
    subgraph Sistem
        S1[Memvalidasi kredensial]
        S2{Kredensial valid?}
        S3[Membuat sesi pengguna]
        S4[Mengarahkan ke Dashboard]
        S5[Menampilkan pesan kesalahan]
    end
    
    P3 --> S1
    S1 --> S2
    S2 -- Ya --> S3
    S3 --> S4
    S4 --> P4
    S2 -- Tidak --> S5
    S5 --> P5
```

---

## 2. Activity Diagram Logout

```mermaid
flowchart TD
    subgraph Pengguna
        P_Start((Start)) --> P1[Mengklik tombol Logout]
        P2[Kembali ke halaman Login] --> P_Stop((Stop))
    end
    subgraph Sistem
        S1[Mengakhiri sesi pengguna]
        S2[Mengarahkan ke halaman Login]
    end
    
    P1 --> S1
    S1 --> S2
    S2 --> P2
```

---

## 3. Activity Diagram Lihat Dashboard

```mermaid
flowchart TD
    subgraph Pengguna
        P_Start((Start)) --> P1[Membuka halaman Dashboard]
        P2[Memantau kondisi persediaan secara real-time] --> P_Stop((Stop))
    end
    subgraph Sistem
        S1[Mengambil data persediaan dari basis data]
        S2[Menghitung barang kritis dan bahan mendekati kadaluarsa]
        S3[Mengambil log aktivitas terbaru]
        S4[Merender grafik distribusi stok dan tren transaksi]
        S5[Menampilkan semua data pada halaman Dashboard]
    end
    
    P1 --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> P2
```

---

## 4. Activity Diagram Kelola Data Barang

```mermaid
flowchart TD
    subgraph Pengguna
        P_Start((Start)) --> P1[Membuka halaman Data Barang]
        P2{Pilih operasi}
        
        P_T1[Mengklik tombol Tambah]
        P_T2[Mengisi dan menyimpan data]
        P_T3[Data baru tampil di tabel] --> P_Stop1((Stop))
        P_T4[Memperbaiki input] --> P_Stop2((Stop))
        
        P_U1[Mengklik ikon edit pada baris data]
        P_U2[Mengubah dan menyimpan data]
        P_U3[Data yang diubah tampil di tabel] --> P_Stop3((Stop))
        P_U4[Memperbaiki input] --> P_Stop4((Stop))
        
        P_H1[Mengklik ikon hapus pada baris data]
        P_H2[Mengonfirmasi penghapusan]
        P_H3[Melihat pesan kesalahan] --> P_Stop5((Stop))
        P_H4[Data terhapus dari tabel] --> P_Stop6((Stop))
    end
    
    subgraph Sistem
        S1[Menampilkan daftar barang dalam format tabel]
        
        S_T1[Menampilkan formulir kosong]
        S_T2{Input valid?}
        S_T3[Menyimpan data ke basis data]
        S_T4[Memicu pembaruan tabel HTMX Reload]
        S_T5[Menampilkan pesan kesalahan]
        
        S_U1[Menampilkan formulir dengan data terisi]
        S_U2{Input valid?}
        S_U3[Memperbarui data di basis data]
        S_U4[Memicu pembaruan tabel HTMX Reload]
        S_U5[Menampilkan pesan kesalahan]
        
        S_H1[Menampilkan konfirmasi penghapusan]
        S_H2{Data masih digunakan?}
        S_H3[Menampilkan pesan Data masih digunakan]
        S_H4[Menghapus data dari basis data]
        S_H5[Memicu pembaruan tabel HTMX Reload]
    end
    
    P1 --> S1
    S1 --> P2
    
    P2 -- Tambah --> P_T1
    P_T1 --> S_T1
    S_T1 --> P_T2
    P_T2 --> S_T2
    S_T2 -- Ya --> S_T3
    S_T3 --> S_T4
    S_T4 --> P_T3
    S_T2 -- Tidak --> S_T5
    S_T5 --> P_T4
    
    P2 -- Ubah --> P_U1
    P_U1 --> S_U1
    S_U1 --> P_U2
    P_U2 --> S_U2
    S_U2 -- Ya --> S_U3
    S_U3 --> S_U4
    S_U4 --> P_U3
    S_U2 -- Tidak --> S_U5
    S_U5 --> P_U4
    
    P2 -- Hapus --> P_H1
    P_H1 --> S_H1
    S_H1 --> P_H2
    P_H2 --> S_H2
    S_H2 -- Ya --> S_H3
    S_H3 --> P_H3
    S_H2 -- Tidak --> S_H4
    S_H4 --> S_H5
    S_H5 --> P_H4
```

---

## 5. Activity Diagram Kelola Kategori

```mermaid
flowchart TD
    subgraph Pengguna
        P_Start((Start)) --> P1[Membuka halaman Kategori]
        P2{Pilih operasi}
        
        P_T1[Mengklik tombol Tambah]
        P_T2[Mengisi dan menyimpan data]
        P_T3[Data baru tampil di tabel] --> P_Stop1((Stop))
        P_T4[Memperbaiki input] --> P_Stop2((Stop))
        
        P_U1[Mengklik ikon edit pada baris data]
        P_U2[Mengubah dan menyimpan data]
        P_U3[Data yang diubah tampil di tabel] --> P_Stop3((Stop))
        P_U4[Memperbaiki input] --> P_Stop4((Stop))
        
        P_H1[Mengklik ikon hapus pada baris data]
        P_H2[Mengonfirmasi penghapusan]
        P_H3[Melihat pesan kesalahan] --> P_Stop5((Stop))
        P_H4[Data terhapus dari tabel] --> P_Stop6((Stop))
    end
    
    subgraph Sistem
        S1[Menampilkan daftar kategori dalam format tabel]
        
        S_T1[Menampilkan formulir kosong]
        S_T2{Input valid?}
        S_T3[Menyimpan data ke basis data]
        S_T4[Memicu pembaruan tabel HTMX Reload]
        S_T5[Menampilkan pesan kesalahan]
        
        S_U1[Menampilkan formulir dengan data terisi]
        S_U2{Input valid?}
        S_U3[Memperbarui data di basis data]
        S_U4[Memicu pembaruan tabel HTMX Reload]
        S_U5[Menampilkan pesan kesalahan]
        
        S_H1[Menampilkan konfirmasi penghapusan]
        S_H2{Data masih digunakan?}
        S_H3[Menampilkan pesan Data masih digunakan]
        S_H4[Menghapus data dari basis data]
        S_H5[Memicu pembaruan tabel HTMX Reload]
    end
    
    P1 --> S1
    S1 --> P2
    
    P2 -- Tambah --> P_T1
    P_T1 --> S_T1
    S_T1 --> P_T2
    P_T2 --> S_T2
    S_T2 -- Ya --> S_T3
    S_T3 --> S_T4
    S_T4 --> P_T3
    S_T2 -- Tidak --> S_T5
    S_T5 --> P_T4
    
    P2 -- Ubah --> P_U1
    P_U1 --> S_U1
    S_U1 --> P_U2
    P_U2 --> S_U2
    S_U2 -- Ya --> S_U3
    S_U3 --> S_U4
    S_U4 --> P_U3
    S_U2 -- Tidak --> S_U5
    S_U5 --> P_U4
    
    P2 -- Hapus --> P_H1
    P_H1 --> S_H1
    S_H1 --> P_H2
    P_H2 --> S_H2
    S_H2 -- Ya --> S_H3
    S_H3 --> P_H3
    S_H2 -- Tidak --> S_H4
    S_H4 --> S_H5
    S_H5 --> P_H4
```

---

## 6. Activity Diagram Kelola Satuan

```mermaid
flowchart TD
    subgraph Pengguna
        P_Start((Start)) --> P1[Membuka halaman Satuan]
        P2{Pilih operasi}
        
        P_T1[Mengklik tombol Tambah]
        P_T2[Mengisi dan menyimpan data]
        P_T3[Data baru tampil di tabel] --> P_Stop1((Stop))
        P_T4[Memperbaiki input] --> P_Stop2((Stop))
        
        P_U1[Mengklik ikon edit pada baris data]
        P_U2[Mengubah dan menyimpan data]
        P_U3[Data yang diubah tampil di tabel] --> P_Stop3((Stop))
        P_U4[Memperbaiki input] --> P_Stop4((Stop))
        
        P_H1[Mengklik ikon hapus pada baris data]
        P_H2[Mengonfirmasi penghapusan]
        P_H3[Melihat pesan kesalahan] --> P_Stop5((Stop))
        P_H4[Data terhapus dari tabel] --> P_Stop6((Stop))
    end
    
    subgraph Sistem
        S1[Menampilkan daftar satuan dalam format tabel]
        
        S_T1[Menampilkan formulir kosong]
        S_T2{Input valid?}
        S_T3[Menyimpan data ke basis data]
        S_T4[Memicu pembaruan tabel HTMX Reload]
        S_T5[Menampilkan pesan kesalahan]
        
        S_U1[Menampilkan formulir dengan data terisi]
        S_U2{Input valid?}
        S_U3[Memperbarui data di basis data]
        S_U4[Memicu pembaruan tabel HTMX Reload]
        S_U5[Menampilkan pesan kesalahan]
        
        S_H1[Menampilkan konfirmasi penghapusan]
        S_H2{Data masih digunakan?}
        S_H3[Menampilkan pesan Data masih digunakan]
        S_H4[Menghapus data dari basis data]
        S_H5[Memicu pembaruan tabel HTMX Reload]
    end
    
    P1 --> S1
    S1 --> P2
    
    P2 -- Tambah --> P_T1
    P_T1 --> S_T1
    S_T1 --> P_T2
    P_T2 --> S_T2
    S_T2 -- Ya --> S_T3
    S_T3 --> S_T4
    S_T4 --> P_T3
    S_T2 -- Tidak --> S_T5
    S_T5 --> P_T4
    
    P2 -- Ubah --> P_U1
    P_U1 --> S_U1
    S_U1 --> P_U2
    P_U2 --> S_U2
    S_U2 -- Ya --> S_U3
    S_U3 --> S_U4
    S_U4 --> P_U3
    S_U2 -- Tidak --> S_U5
    S_U5 --> P_U4
    
    P2 -- Hapus --> P_H1
    P_H1 --> S_H1
    S_H1 --> P_H2
    P_H2 --> S_H2
    S_H2 -- Ya --> S_H3
    S_H3 --> P_H3
    S_H2 -- Tidak --> S_H4
    S_H4 --> S_H5
    S_H5 --> P_H4
```

---

## 7. Activity Diagram Catat Barang Masuk

```mermaid
flowchart TD
    subgraph Pengguna
        P_Start((Start)) --> P1[Membuka halaman Log Barang Masuk]
        P1 --> P2[Mengklik tombol Catat Barang Masuk]
        P3[Memilih barang]
        P3 --> P4[Mengisi jumlah, pemasok, dan tanggal kadaluarsa]
        P4 --> P5[Menekan tombol Simpan]
        P6[Transaksi masuk tercatat pada tabel] --> P_Stop1((Stop))
        P7[Memperbaiki input] --> P_Stop2((Stop))
    end
    subgraph Sistem
        S1[Menampilkan formulir]
        S2{Input valid?}
        S3[Menambah jumlah ke stok terkini Barang]
        S4[Membuat catatan batch baru StokBatch]
        S5[Menyimpan log transaksi masuk]
        S6[Memperbarui tabel riwayat]
        S7[Menampilkan pesan kesalahan]
    end
    
    P2 --> S1
    S1 --> P3
    P5 --> S2
    S2 -- Ya --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> P6
    S2 -- Tidak --> S7
    S7 --> P7
```

---

## 8. Activity Diagram Catat Barang Keluar

```mermaid
flowchart TD
    subgraph Pengguna
        P_Start((Start)) --> P1[Membuka halaman Log Barang Keluar]
        P1 --> P2[Mengklik tombol Catat Barang Keluar]
        P3[Memilih barang, mengisi jumlah dan alasan pengeluaran]
        P3 --> P4[Menekan tombol Simpan]
        P5[Transaksi keluar tercatat pada tabel] --> P_Stop1((Stop))
        P6[Melihat pesan kesalahan] --> P_Stop2((Stop))
    end
    subgraph Sistem
        S1[Menampilkan formulir]
        S2{Stok mencukupi?}
        S3[Mengambil dan mengurutkan batch berdasarkan kadaluarsa terdekat dan waktu pembuatan]
        S4[Memotong stok batch satu per satu hingga jumlah terpenuhi FIFO]
        S5[Mencatat relasi pemotongan batch BarangKeluarBatch]
        S6[Memperbarui stok terkini Barang]
        S7[Menyimpan log transaksi keluar]
        S8[Memperbarui tabel riwayat]
        S9[Menampilkan pesan Stok tidak mencukupi]
    end
    
    P2 --> S1
    S1 --> P3
    P4 --> S2
    S2 -- Ya --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
    S7 --> S8
    S8 --> P5
    S2 -- Tidak --> S9
    S9 --> P6
```

---

## 9. Activity Diagram Lihat Buku Besar

```mermaid
flowchart TD
    subgraph Pengguna
        P_Start((Start)) --> P1[Membuka halaman Buku Besar]
        P2[Melihat tabel transaksi]
        P2 --> P3[Menerapkan filter rentang tanggal atau jenis transaksi opsional]
        P4[Melihat data yang terfilter] --> P_Stop((Stop))
    end
    subgraph Sistem
        S1[Mengambil seluruh data transaksi dari basis data]
        S2[Menampilkan rekap transaksi masuk dan keluar secara kronologis]
        S3[Memproses filter]
        S4[Memperbarui tabel sesuai filter]
    end
    
    P1 --> S1
    S1 --> S2
    S2 --> P2
    P3 --> S3
    S3 --> S4
    S4 --> P4
```

---

## 10. Activity Diagram Ekspor Laporan

```mermaid
flowchart TD
    subgraph Pengguna
        P_Start((Start)) --> P1[Berada di halaman Buku Besar]
        P1 --> P2[Mengklik tombol Export CSV atau Export PDF]
        P3[Menyimpan file laporan ke perangkat] --> P_Stop((Stop))
    end
    subgraph Sistem
        S1[Mengumpulkan data transaksi sesuai filter aktif]
        S2{Format CSV?}
        S3[Menghasilkan file .csv dengan kolom terstruktur]
        S4[Mengonversi template laporan menjadi dokumen PDF]
        S5[Mengirim file ke peramban untuk diunduh]
    end
    
    P2 --> S1
    S1 --> S2
    S2 -- Ya --> S3
    S2 -- Tidak PDF --> S4
    S3 --> S5
    S4 --> S5
    S5 --> P3
```
