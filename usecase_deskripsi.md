# Deskripsi Use Case Sistem Informasi Persediaan Rumah Makan Aisyah Ngabang

---

Use case berikut menggambarkan seluruh interaksi yang dapat dilakukan oleh aktor Pengguna terhadap sistem informasi persediaan Rumah Makan Aisyah Ngabang. Pengguna merupakan satu-satunya aktor dalam sistem ini, yaitu pemilik atau pengelola rumah makan yang bertanggung jawab atas seluruh aktivitas pencatatan dan pemantauan persediaan bahan baku.

---

Use case Login menggambarkan proses autentikasi yang wajib dilalui oleh Pengguna sebelum dapat mengakses fitur apapun dalam sistem. Sistem hanya memberikan akses kepada pengguna yang memiliki kredensial yang valid, sehingga seluruh data persediaan terlindungi dari akses yang tidak sah.

## Tabel 5.X Deskripsi Use Case Login

| | |
|---|---|
| **Nama Use Case** | Login |
| **Aktor** | Pengguna |
| **Pre-kondisi** | Pengguna belum terautentikasi dan mengakses sistem melalui peramban web. |
| **Flow of Event** | 1. Pengguna membuka sistem melalui peramban web. |
| | 2. Sistem menampilkan halaman Login. |
| | 3. Pengguna memasukkan nama pengguna dan kata sandi. |
| | 4. Pengguna menekan tombol Login. |
| | 5. Sistem memvalidasi kredensial yang dimasukkan. |
| | 6. Jika kredensial valid, sistem mengarahkan pengguna ke halaman Dashboard. |
| | 7. Jika kredensial tidak valid, sistem menampilkan pesan kesalahan dan pengguna diminta mengulang. |
| **Post-kondisi** | Pengguna berhasil masuk ke sistem dan dapat mengakses seluruh fitur yang tersedia. |

---

Use case Logout menggambarkan proses pengakhiran sesi yang dilakukan oleh Pengguna setelah selesai menggunakan sistem. Setelah logout, seluruh halaman sistem tidak dapat diakses kembali hingga pengguna melakukan login ulang.

## Tabel 5.X Deskripsi Use Case Logout

| | |
|---|---|
| **Nama Use Case** | Logout |
| **Aktor** | Pengguna |
| **Pre-kondisi** | Pengguna telah login dan sedang menggunakan sistem. |
| **Flow of Event** | 1. Pengguna mengklik tombol Logout pada antarmuka sistem. |
| | 2. Sistem mengakhiri sesi pengguna yang aktif. |
| | 3. Sistem mengarahkan pengguna kembali ke halaman Login. |
| **Post-kondisi** | Sesi pengguna berakhir dan seluruh halaman sistem tidak dapat diakses hingga login kembali. |

---

Use case Lihat Dashboard menggambarkan interaksi Pengguna dalam memantau kondisi persediaan secara keseluruhan melalui halaman utama sistem. Halaman ini menjadi pusat informasi yang menyajikan ringkasan stok kritis, peringatan kadaluarsa, log aktivitas transaksi terbaru, dan visualisasi grafik persediaan secara real-time.

## Tabel 5.X Deskripsi Use Case Lihat Dashboard

| | |
|---|---|
| **Nama Use Case** | Lihat Dashboard |
| **Aktor** | Pengguna |
| **Pre-kondisi** | Pengguna telah berhasil login ke dalam sistem. |
| **Flow of Event** | 1. Pengguna mengakses halaman Dashboard. |
| | 2. Sistem mengambil data persediaan terkini dari basis data. |
| | 3. Sistem menampilkan kartu ringkasan yang memuat jumlah barang dengan stok kritis dan jumlah bahan baku yang mendekati kadaluarsa dalam 7 hari ke depan. |
| | 4. Sistem menampilkan panel peringatan dini berisi daftar barang kritis beserta sisa stoknya. |
| | 5. Sistem menampilkan log aktivitas transaksi terbaru secara kronologis. |
| | 6. Sistem merender grafik Doughnut distribusi stok per kategori dan grafik Line tren transaksi masuk dan keluar. |
| **Post-kondisi** | Pengguna mendapatkan gambaran menyeluruh kondisi persediaan secara real-time. |

---

Use case Kelola Data Master menggambarkan interaksi Pengguna dalam mengelola data referensi utama sistem, yaitu data Barang, Kategori, dan Satuan. Aktivitas yang dapat dilakukan mencakup penambahan data baru, pengubahan data yang sudah ada, dan penghapusan data yang tidak lagi digunakan. Seluruh operasi ini dilakukan melalui formulir yang muncul tanpa perlu memuat ulang halaman.

## Tabel 5.X Deskripsi Use Case Kelola Data Master

| | |
|---|---|
| **Nama Use Case** | Kelola Data Master |
| **Aktor** | Pengguna |
| **Pre-kondisi** | Pengguna telah berhasil login ke dalam sistem. |
| **Flow of Event** | 1. Pengguna membuka halaman Barang, Kategori, atau Satuan. |
| | 2. Sistem menampilkan daftar data dalam format tabel. |
| | 3. Untuk menambah data, pengguna mengklik tombol Tambah, mengisi formulir yang muncul, lalu menekan Simpan. Sistem memvalidasi input, menyimpan data ke basis data, dan memperbarui tabel secara otomatis. |
| | 4. Untuk mengubah data, pengguna mengklik ikon edit pada baris yang dituju. Sistem menampilkan formulir dengan data yang sudah terisi. Pengguna melakukan perubahan dan menekan Simpan. Sistem memperbarui data dan menyegarkan tampilan tabel. |
| | 5. Untuk menghapus data, pengguna mengklik ikon hapus pada baris yang dituju. Sistem menampilkan konfirmasi penghapusan. Jika data tidak sedang digunakan, sistem menghapus data dan memperbarui tabel. Jika data masih digunakan, sistem menampilkan pesan kesalahan dan membatalkan penghapusan. |
| **Post-kondisi** | Data master (Barang, Kategori, atau Satuan) berhasil ditambah, diubah, atau dihapus sesuai operasi yang dilakukan. |

---

Use case Catat Barang Masuk menggambarkan interaksi Pengguna dalam merekam penerimaan bahan baku ke dalam sistem. Setiap pencatatan barang masuk secara otomatis menambah nilai stok terkini dan membuat catatan batch baru yang menjadi dasar penerapan logika FIFO pada saat pengeluaran barang.

## Tabel 5.X Deskripsi Use Case Catat Barang Masuk

| | |
|---|---|
| **Nama Use Case** | Catat Barang Masuk |
| **Aktor** | Pengguna |
| **Pre-kondisi** | Pengguna telah berhasil login dan data barang yang akan dicatat sudah terdaftar di sistem. |
| **Flow of Event** | 1. Pengguna membuka halaman Log Barang Masuk. |
| | 2. Pengguna mengklik tombol Catat Barang Masuk. |
| | 3. Sistem menampilkan formulir tanpa memuat ulang halaman. |
| | 4. Pengguna memilih barang, mengisi jumlah yang diterima, nama pemasok, dan tanggal kadaluarsa (jika ada). |
| | 5. Pengguna menekan tombol Simpan. |
| | 6. Sistem memvalidasi input yang dimasukkan. |
| | 7. Sistem menambahkan jumlah yang diterima ke nilai stok terkini pada data master Barang. |
| | 8. Sistem membuat catatan batch baru untuk melacak kelompok stok ini secara terpisah. |
| | 9. Sistem menyimpan catatan transaksi masuk sebagai log permanen. |
| | 10. Sistem menutup formulir dan memperbarui tabel riwayat transaksi. |
| **Post-kondisi** | Stok barang bertambah, data batch baru tercatat, dan riwayat transaksi masuk tersimpan di sistem. |

---

Use case Catat Barang Keluar menggambarkan interaksi Pengguna dalam merekam pengeluaran bahan baku dari persediaan. Proses ini merupakan use case terpenting karena melibatkan validasi kecukupan stok secara otomatis dan penerapan logika FIFO, di mana bahan baku dengan tanggal kadaluarsa terdekat selalu dikeluarkan terlebih dahulu untuk meminimalkan risiko kerugian akibat bahan baku kadaluarsa.

## Tabel 5.X Deskripsi Use Case Catat Barang Keluar

| | |
|---|---|
| **Nama Use Case** | Catat Barang Keluar |
| **Aktor** | Pengguna |
| **Pre-kondisi** | Pengguna telah berhasil login dan barang yang akan dikeluarkan memiliki stok yang mencukupi. |
| **Flow of Event** | 1. Pengguna membuka halaman Log Barang Keluar. |
| | 2. Pengguna mengklik tombol Catat Barang Keluar. |
| | 3. Sistem menampilkan formulir tanpa memuat ulang halaman. |
| | 4. Pengguna memilih barang, mengisi jumlah yang dikeluarkan, dan memilih alasan pengeluaran (Pemakaian Dapur, Rusak, Kadaluarsa, atau Lainnya). |
| | 5. Pengguna menekan tombol Simpan. |
| | 6. Sistem memvalidasi kecukupan stok. Jika stok tidak mencukupi, sistem menampilkan pesan kesalahan dan transaksi dibatalkan. |
| | 7. Jika stok mencukupi, sistem menjalankan logika FIFO: memotong stok dari batch dengan tanggal kadaluarsa terdekat terlebih dahulu, dilanjutkan ke batch berikutnya hingga jumlah terpenuhi. |
| | 8. Sistem memperbarui nilai stok terkini pada data master Barang. |
| | 9. Sistem menyimpan catatan transaksi keluar sebagai log permanen. |
| | 10. Sistem menutup formulir dan memperbarui tabel riwayat transaksi. |
| **Post-kondisi** | Stok barang berkurang sesuai jumlah yang dikeluarkan dengan urutan batch FIFO, dan riwayat transaksi keluar tersimpan di sistem. |

---

Use case Lihat Buku Besar menggambarkan interaksi Pengguna dalam mengakses riwayat gabungan seluruh transaksi masuk dan keluar secara kronologis dalam satu tampilan terpadu. Pengguna dapat menyaring data berdasarkan rentang tanggal dan jenis transaksi untuk memudahkan penelusuran dan rekapitulasi data persediaan.

## Tabel 5.X Deskripsi Use Case Lihat Buku Besar

| | |
|---|---|
| **Nama Use Case** | Lihat Buku Besar |
| **Aktor** | Pengguna |
| **Pre-kondisi** | Pengguna telah berhasil login ke dalam sistem. |
| **Flow of Event** | 1. Pengguna membuka halaman Buku Besar. |
| | 2. Sistem menampilkan rekap gabungan seluruh transaksi masuk dan keluar secara kronologis dalam format tabel. |
| | 3. Pengguna dapat menggunakan fitur filter untuk menyaring data berdasarkan rentang tanggal atau jenis transaksi. |
| | 4. Sistem memperbarui tabel sesuai kriteria filter yang dipilih. |
| **Post-kondisi** | Pengguna dapat melihat riwayat seluruh transaksi persediaan secara lengkap dan terfilter sesuai kebutuhan. |

---

Use case Ekspor Laporan menggambarkan interaksi Pengguna dalam mengunduh laporan transaksi dari halaman Buku Besar ke dalam format file yang dapat disimpan dan dibagikan. Sistem mendukung dua format ekspor, yaitu CSV untuk keperluan pengolahan data di aplikasi spreadsheet, dan PDF untuk keperluan dokumentasi dan arsip formal.

## Tabel 5.X Deskripsi Use Case Ekspor Laporan

| | |
|---|---|
| **Nama Use Case** | Ekspor Laporan |
| **Aktor** | Pengguna |
| **Pre-kondisi** | Pengguna telah berhasil login dan berada di halaman Buku Besar. |
| **Flow of Event** | **Ekspor CSV** |
| | 1. Pengguna mengklik tombol Export CSV pada halaman Buku Besar. |
| | 2. Sistem mengumpulkan data transaksi sesuai filter yang aktif. |
| | 3. Sistem menghasilkan file berformat .csv dengan kolom-kolom yang terstruktur. |
| | 4. Peramban mengunduh file CSV ke perangkat pengguna. |
| | **Ekspor PDF** |
| | 1. Pengguna mengklik tombol Export PDF pada halaman Buku Besar. |
| | 2. Sistem mengumpulkan data transaksi sesuai filter yang aktif. |
| | 3. Sistem mengonversi template laporan menjadi dokumen PDF. |
| | 4. Peramban mengunduh file PDF ke perangkat pengguna. |
| **Post-kondisi** | File laporan (CSV atau PDF) berhasil diunduh dan dapat dibuka untuk keperluan dokumentasi atau audit. |
