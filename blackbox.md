#### 5.1.4.1 Pengujian *Blackbox Testing*

Metode pengujian yang digunakan pada fase *Cutover* adalah *Blackbox Testing* (Pengujian Kotak Hitam). Pendekatan ini berfokus pada pengamatan terhadap keluaran (*output*) sistem berdasarkan masukan (*input*) yang diberikan, tanpa memperhatikan bagaimana mekanisme internal sistem memproses data tersebut. Dengan kata lain, pengujian dilakukan murni dari sudut pandang pengguna untuk memverifikasi bahwa setiap fitur dan fungsi sistem menghasilkan respons yang tepat, akurat, dan konsisten.

Pengujian dibagi ke dalam beberapa kelompok alur fungsional yang mencakup seluruh modul yang telah diimplementasikan pada sistem. Setiap kelompok alur memiliki skenario pengujian tersendiri yang disusun berdasarkan interaksi pengguna yang paling mungkin terjadi dalam kondisi operasional nyata.

---

##### a. Alur Autentikasi (Login dan Logout)

Pengujian pada alur autentikasi bertujuan untuk memverifikasi bahwa sistem mampu membatasi hak akses secara tepat. Hanya pengguna yang memiliki kredensial yang sah yang diperbolehkan masuk ke dalam sistem. Pengujian ini juga memastikan bahwa mekanisme keamanan sesi (*session*) berjalan dengan benar, sehingga pengguna yang belum terautentikasi tidak dapat mengakses halaman mana pun di dalam aplikasi secara langsung. Selain itu, diuji pula apakah proses logout berhasil mengakhiri sesi dan mencegah pengguna kembali mengakses halaman internal tanpa login ulang.

[Tabel Pengujian Alur Autentikasi]

KOLOM: No | Nama Pengujian | Skenario Uji | Data Input | Hasil yang Diharapkan | Hasil Pengujian | Status

1 | Login dengan kredensial valid | Pengguna mengisi username dan password yang benar lalu menekan tombol Masuk | Username: admin, Password: [benar] | Sistem mengautentikasi pengguna dan mengarahkan ke halaman Dashboard | Sesuai harapan | Berhasil

2 | Login dengan password salah | Pengguna mengisi username yang benar namun password yang salah | Username: admin, Password: [salah] | Sistem menampilkan pesan peringatan bahwa username atau password tidak valid dan pengguna tetap di halaman Login | Sesuai harapan | Berhasil

3 | Login dengan username yang tidak terdaftar | Pengguna mengisi username yang tidak ada di sistem | Username: userpalsu, Password: apapun | Sistem menampilkan pesan peringatan dan menolak proses login | Sesuai harapan | Berhasil

4 | Login dengan form kosong | Pengguna menekan tombol Masuk tanpa mengisi field apapun | Username: (kosong), Password: (kosong) | Sistem menampilkan pesan validasi bahwa field tidak boleh kosong | Sesuai harapan | Berhasil

5 | Akses halaman internal tanpa login | Pengguna mencoba membuka URL halaman Dashboard secara langsung tanpa sesi login aktif | URL: /dashboard/ | Sistem menolak akses dan mengalihkan pengguna ke halaman Login | Sesuai harapan | Berhasil

6 | Logout dari sistem | Pengguna menekan tombol Keluar pada menu profil di topbar | Klik tombol Keluar | Sistem mengakhiri sesi pengguna dan mengalihkan ke halaman Login | Sesuai harapan | Berhasil

7 | Akses halaman internal setelah logout | Pengguna menekan tombol back pada browser setelah berhasil logout | Klik tombol back browser setelah logout | Sistem tetap menolak akses dan mengalihkan kembali ke halaman Login | Sesuai harapan | Berhasil

---

##### b. Alur Pengelolaan Data Kategori

Pengujian alur pengelolaan data kategori bertujuan untuk memverifikasi bahwa operasi penambahan, pengubahan, dan penghapusan data kategori berjalan dengan benar. Selain itu, pengujian ini juga mencakup validasi integritas data referensial, yakni memastikan bahwa sistem melindungi data kategori yang masih terikat dengan data barang agar tidak dapat dihapus secara sembarangan, sehingga konsistensi data dalam basis data selalu terjaga.

[Tabel Pengujian Alur Kelola Kategori]

KOLOM: No | Nama Pengujian | Skenario Uji | Data Input | Hasil yang Diharapkan | Hasil Pengujian | Status

1 | Menambah kategori baru dengan data valid | Admin mengisi form tambah kategori dengan nama yang belum terdaftar dan menekan Simpan | Nama: Protein Hewani, Deskripsi: Daging dan sejenisnya | Sistem menyimpan data ke database, menampilkan notifikasi keberhasilan, dan data baru muncul di daftar kategori | Sesuai harapan | Berhasil

2 | Menambah kategori dengan nama yang sudah ada (duplikat) | Admin mengisi form tambah kategori dengan nama yang telah terdaftar | Nama: Protein Hewani (sudah ada) | Sistem menampilkan pesan error validasi bahwa nama kategori sudah terdaftar dan menolak penyimpanan | Sesuai harapan | Berhasil

3 | Menambah kategori dengan nama kosong | Admin menekan simpan tanpa mengisi field nama | Nama: (kosong) | Sistem menampilkan pesan validasi bahwa field nama wajib diisi | Sesuai harapan | Berhasil

4 | Mengubah nama kategori yang sudah ada | Admin membuka form edit kategori, mengubah namanya, dan menekan Simpan | Nama diubah dari: Protein Hewani menjadi: Protein | Sistem memperbarui data di database, menampilkan notifikasi keberhasilan, dan perubahan terlihat pada daftar | Sesuai harapan | Berhasil

5 | Menghapus kategori yang tidak memiliki barang | Admin menghapus data kategori yang tidak terikat dengan data barang manapun | Klik Hapus pada kategori yang kosong | Sistem berhasil menghapus data kategori dan menampilkan notifikasi keberhasilan | Sesuai harapan | Berhasil

6 | Menghapus kategori yang masih digunakan oleh data barang | Admin mencoba menghapus kategori yang masih memiliki barang terikat | Klik Hapus pada Kategori: Protein (masih dipakai) | Sistem menolak penghapusan dan menampilkan pesan error bahwa kategori tidak dapat dihapus karena masih digunakan | Sesuai harapan | Berhasil

---

##### c. Alur Pengelolaan Data Satuan

Pengujian alur pengelolaan data satuan bertujuan untuk memverifikasi bahwa operasi CRUD (Create, Read, Update, Delete) pada modul satuan barang berjalan sebagaimana mestinya. Sama halnya dengan kategori, sistem juga harus mampu melindungi data satuan yang masih aktif digunakan oleh data barang agar tidak terhapus, karena penghapusan data satuan yang masih terikat akan menyebabkan kerusakan integritas data pada tabel barang.

[Tabel Pengujian Alur Kelola Satuan]

KOLOM: No | Nama Pengujian | Skenario Uji | Data Input | Hasil yang Diharapkan | Hasil Pengujian | Status

1 | Menambah satuan baru dengan data valid | Admin mengisi form tambah satuan dengan nama yang belum terdaftar | Nama Satuan: Kilogram | Sistem menyimpan data satuan baru dan menampilkan notifikasi keberhasilan | Sesuai harapan | Berhasil

2 | Menambah satuan dengan nama duplikat | Admin mencoba mendaftarkan nama satuan yang sudah ada | Nama Satuan: Kilogram (sudah ada) | Sistem menampilkan pesan error validasi dan menolak penyimpanan | Sesuai harapan | Berhasil

3 | Mengubah nama satuan yang sudah ada | Admin membuka form edit, mengubah nama satuan, dan menekan Simpan | Nama diubah dari: Kilogram menjadi: Kg | Sistem memperbarui data dan menampilkan notifikasi keberhasilan | Sesuai harapan | Berhasil

4 | Menghapus satuan yang tidak terikat barang | Admin menghapus data satuan yang tidak digunakan oleh barang manapun | Klik Hapus pada satuan yang tidak terpakai | Sistem berhasil menghapus dan menampilkan notifikasi keberhasilan | Sesuai harapan | Berhasil

5 | Menghapus satuan yang masih digunakan oleh data barang | Admin mencoba menghapus satuan yang masih terikat pada data barang | Klik Hapus pada Satuan: Kg (masih dipakai) | Sistem menolak penghapusan dan menampilkan pesan error perlindungan integritas data | Sesuai harapan | Berhasil

---

##### d. Alur Pengelolaan Data Barang

Pengujian alur pengelolaan data barang bertujuan untuk memverifikasi bahwa modul data master barang, yang merupakan entitas inti dari sistem persediaan, dapat beroperasi secara penuh. Pengujian mencakup operasi tambah, ubah, dan cari barang, termasuk memastikan bahwa nilai stok awal dikelola dengan benar oleh sistem serta fitur penyaringan berdasarkan kategori berjalan dengan akurat.

[Tabel Pengujian Alur Kelola Data Barang]

KOLOM: No | Nama Pengujian | Skenario Uji | Data Input | Hasil yang Diharapkan | Hasil Pengujian | Status

1 | Menambah data barang baru | Admin mengisi seluruh field form tambah barang dengan data valid dan menekan Simpan | Nama: Daging Ayam, Kategori: Protein, Satuan: Kg, Stok Minimal: 5 | Sistem menyimpan data barang baru, stok awal tercatat 0, data muncul di daftar barang | Sesuai harapan | Berhasil

2 | Menambah barang dengan field wajib kosong | Admin menekan simpan tanpa mengisi salah satu field wajib | Nama: (kosong), Kategori: dipilih, Satuan: dipilih | Sistem menampilkan pesan validasi bahwa field nama wajib diisi | Sesuai harapan | Berhasil

3 | Mengubah data barang (stok minimal) | Admin membuka form edit barang dan mengubah nilai stok minimal | Stok Minimal Daging Ayam diubah dari 5 menjadi 10 | Sistem memperbarui data dan menampilkan notifikasi keberhasilan, perubahan terlihat pada daftar | Sesuai harapan | Berhasil

4 | Mencari barang berdasarkan nama | Admin mengetikkan nama barang pada kolom pencarian di halaman Data Barang | Kata kunci: Ayam | Sistem menampilkan hanya barang-barang yang mengandung kata Ayam pada namanya | Sesuai harapan | Berhasil

5 | Memfilter barang berdasarkan kategori | Admin memilih salah satu kategori pada dropdown filter | Filter Kategori: Protein | Sistem hanya menampilkan barang yang termasuk kategori Protein | Sesuai harapan | Berhasil

6 | Mencari barang dengan kata kunci yang tidak cocok | Admin mengetikkan nama barang yang tidak terdaftar | Kata kunci: XYZ123 | Sistem menampilkan halaman kosong atau pesan bahwa tidak ada data yang ditemukan | Sesuai harapan | Berhasil

---

##### e. Alur Pencatatan Barang Masuk

Pengujian alur pencatatan barang masuk bertujuan untuk memverifikasi bahwa setiap kali terjadi penerimaan bahan baku dari pemasok, sistem mampu mencatat transaksi dengan benar, memperbarui total stok secara akurat, dan secara otomatis membuat entri *StokBatch* baru yang akan menjadi fondasi operasional algoritma FIFO. Pengujian juga memastikan bahwa field tanggal kadaluarsa yang bersifat opsional dapat dikosongkan tanpa menyebabkan kesalahan pada sistem.

[Tabel Pengujian Alur Barang Masuk]

KOLOM: No | Nama Pengujian | Skenario Uji | Data Input | Hasil yang Diharapkan | Hasil Pengujian | Status

1 | Mencatat barang masuk dengan data lengkap | Admin mengisi seluruh field form barang masuk termasuk tanggal kadaluarsa | Barang: Daging Ayam, Jumlah: 20, Supplier: UD Maju, Tanggal: hari ini, Kadaluarsa: 25 Jun 2026 | Sistem mencatat transaksi, stok Daging Ayam bertambah 20 Kg, dan satu entri StokBatch baru terbuat secara otomatis | Sesuai harapan | Berhasil

2 | Mencatat barang masuk tanpa tanggal kadaluarsa | Admin mengisi form barang masuk tanpa mengisi field tanggal kadaluarsa | Barang: Garam, Jumlah: 10, Supplier: Toko ABC, Kadaluarsa: (kosong) | Sistem berhasil menyimpan transaksi dan membuat StokBatch baru tanpa tanggal kadaluarsa | Sesuai harapan | Berhasil

3 | Mencatat barang masuk dengan jumlah nol | Admin mengisi jumlah dengan nilai 0 | Barang: Beras, Jumlah: 0 | Sistem menampilkan pesan validasi bahwa jumlah harus lebih besar dari 0 | Sesuai harapan | Berhasil

4 | Memverifikasi pembaruan stok setelah transaksi masuk | Admin mengecek total stok barang di halaman Data Barang setelah mencatat barang masuk | Setelah mencatat 20 Kg Daging Ayam masuk (stok awal 0) | Halaman Data Barang menampilkan stok Daging Ayam sebesar 20 Kg | Sesuai harapan | Berhasil

5 | Mencatat dua transaksi masuk untuk barang yang sama (dua batch berbeda) | Admin mencatat barang masuk untuk barang yang sama sebanyak dua kali dengan tanggal kadaluarsa yang berbeda | Daging Ayam masuk 10 Kg exp. 20 Jun, lalu masuk lagi 15 Kg exp. 30 Jun | Sistem membuat dua entri StokBatch terpisah dan total stok Daging Ayam menjadi 25 Kg | Sesuai harapan | Berhasil

---

##### f. Alur Pencatatan Barang Keluar dan Verifikasi Algoritma FIFO

Pengujian alur pencatatan barang keluar merupakan pengujian paling krusial dalam sistem ini karena mencakup verifikasi terhadap beroperasinya algoritma FIFO secara otomatis. Tujuan pengujian adalah untuk membuktikan bahwa sistem mampu memotong stok dari *batch* dengan tanggal kadaluarsa paling awal terlebih dahulu tanpa intervensi manual dari pengguna, mampu melanjutkan pemotongan stok ke *batch* berikutnya apabila stok *batch* pertama tidak mencukupi, serta menolak transaksi apabila total stok barang tidak memadai untuk memenuhi permintaan pengeluaran.

[Tabel Pengujian Alur Barang Keluar dan FIFO]

KOLOM: No | Nama Pengujian | Skenario Uji | Data Input | Hasil yang Diharapkan | Hasil Pengujian | Status

1 | Mencatat barang keluar dengan stok mencukupi | Admin mencatat pengeluaran barang dengan jumlah yang tidak melebihi total stok tersedia | Barang: Daging Ayam, Jumlah: 5, Alasan: Pemakaian Dapur | Sistem berhasil mencatat transaksi, stok Daging Ayam berkurang 5 Kg, dan notifikasi keberhasilan ditampilkan | Sesuai harapan | Berhasil

2 | Mencatat barang keluar dengan jumlah melebihi stok | Admin mencoba mencatat pengeluaran dengan jumlah lebih besar dari stok yang tersedia | Barang: Daging Ayam (stok: 25 Kg), Jumlah Keluar: 9999 | Sistem menolak transaksi dan menampilkan pesan error stok tidak mencukupi, data tidak tersimpan | Sesuai harapan | Berhasil

3 | Verifikasi FIFO: pemotongan dari batch kadaluarsa paling awal | Admin mencatat pengeluaran pada barang yang memiliki dua batch aktif dengan tanggal kadaluarsa berbeda | Batch A: 10 Kg exp. 20 Jun | Batch B: 15 Kg exp. 30 Jun | Keluar: 7 Kg | Sistem memotong 7 Kg dari Batch A (exp. paling awal), Batch A menjadi 3 Kg, Batch B tetap 15 Kg | Sesuai harapan | Berhasil

4 | Verifikasi FIFO: pemotongan berlanjut ke batch berikutnya | Admin mencatat pengeluaran dengan jumlah yang melebihi sisa stok batch pertama namun mencukupi dari total kedua batch | Batch A: 10 Kg exp. 20 Jun | Batch B: 15 Kg exp. 30 Jun | Keluar: 12 Kg | Sistem menghabiskan Batch A (10 Kg) terlebih dahulu lalu memotong sisa 2 Kg dari Batch B, sehingga Batch A menjadi 0 Kg dan Batch B menjadi 13 Kg | Sesuai harapan | Berhasil

5 | Mencatat barang keluar dengan alasan Rusak | Admin mencatat pengeluaran dengan memilih alasan Rusak/Tidak Layak | Barang: Minyak Goreng, Jumlah: 2, Alasan: Rusak / Tidak Layak | Sistem mencatat transaksi dengan alasan yang benar dan stok berkurang sesuai | Sesuai harapan | Berhasil

6 | Mencatat barang keluar dengan alasan Kadaluarsa | Admin mencatat pengeluaran dengan memilih alasan Kadaluarsa | Barang: Susu, Jumlah: 3, Alasan: Kadaluarsa | Sistem mencatat transaksi dengan alasan yang benar dan stok berkurang sesuai | Sesuai harapan | Berhasil

---

##### g. Alur Melihat dan Memfilter Log Ledger (Buku Besar)

Pengujian alur buku besar bertujuan untuk memverifikasi bahwa sistem mampu menampilkan riwayat seluruh transaksi masuk dan keluar secara kronologis. Pengujian juga mencakup fitur penyaringan data (*filter*) berdasarkan rentang tanggal, kata kunci nama barang, dan jenis transaksi, sehingga pengguna maupun pemilik rumah makan dapat dengan cepat menemukan informasi transaksi yang dibutuhkan untuk keperluan audit atau rekonsiliasi stok.

[Tabel Pengujian Alur Log Ledger]

KOLOM: No | Nama Pengujian | Skenario Uji | Data Input | Hasil yang Diharapkan | Hasil Pengujian | Status

1 | Melihat seluruh log ledger tanpa filter | Admin membuka halaman Log Ledger tanpa menerapkan filter apapun | Klik menu Log Ledger | Sistem menampilkan seluruh riwayat transaksi masuk dan keluar secara kronologis dari yang terbaru | Sesuai harapan | Berhasil

2 | Memfilter ledger berdasarkan rentang tanggal | Admin mengisi field tanggal awal dan tanggal akhir lalu menekan tombol filter | Tanggal Awal: 01 Jun 2026, Tanggal Akhir: 17 Jun 2026 | Sistem hanya menampilkan transaksi dalam rentang tanggal yang dipilih, transaksi di luar rentang disaring | Sesuai harapan | Berhasil

3 | Memfilter ledger berdasarkan kata kunci nama barang | Admin mengetikkan nama barang pada kolom pencarian | Kata Kunci: Daging Ayam | Sistem hanya menampilkan transaksi yang berkaitan dengan barang Daging Ayam | Sesuai harapan | Berhasil

4 | Memfilter ledger berdasarkan jenis transaksi (Masuk) | Admin memilih opsi filter Masuk pada dropdown jenis transaksi | Tipe: Masuk | Sistem hanya menampilkan transaksi barang masuk dan menyembunyikan transaksi barang keluar | Sesuai harapan | Berhasil

5 | Memfilter ledger berdasarkan jenis transaksi (Keluar) | Admin memilih opsi filter Keluar pada dropdown jenis transaksi | Tipe: Keluar | Sistem hanya menampilkan transaksi barang keluar dan menyembunyikan transaksi barang masuk | Sesuai harapan | Berhasil

6 | Menerapkan kombinasi filter tanggal dan kata kunci sekaligus | Admin mengisi filter tanggal dan kata kunci secara bersamaan | Tanggal: 01-17 Jun 2026 dan Kata Kunci: Ayam | Sistem menampilkan hanya transaksi Daging Ayam dalam rentang tanggal yang dipilih | Sesuai harapan | Berhasil

---

##### h. Alur Ekspor Laporan

Pengujian alur ekspor laporan bertujuan untuk memverifikasi bahwa sistem mampu menghasilkan dan mengunduh berkas laporan transaksi dalam format yang dapat dibaca dan digunakan lebih lanjut. Pengujian memastikan bahwa berkas CSV yang dihasilkan memiliki format kolom yang lengkap dan karakter yang terbaca dengan benar, serta berkas PDF yang dihasilkan memiliki tampilan yang rapi dan layak cetak sebagai dokumen resmi laporan persediaan rumah makan.

[Tabel Pengujian Alur Ekspor Laporan]

KOLOM: No | Nama Pengujian | Skenario Uji | Data Input | Hasil yang Diharapkan | Hasil Pengujian | Status

1 | Mengekspor seluruh data ke format CSV | Admin menekan tombol Ekspor CSV tanpa filter aktif | Klik tombol Ekspor CSV | Browser mengunduh file CSV berisi seluruh data transaksi dengan kolom lengkap (Tanggal, Nama Barang, Kategori, Tipe, Jumlah, Satuan, Detail, Keterangan) | Sesuai harapan | Berhasil

2 | Mengekspor data yang sudah difilter ke format CSV | Admin menerapkan filter tanggal terlebih dahulu lalu menekan Ekspor CSV | Filter: 01-17 Jun 2026, lalu klik Ekspor CSV | File CSV yang diunduh hanya berisi transaksi dalam rentang tanggal yang dipilih, sesuai dengan tampilan di layar | Sesuai harapan | Berhasil

3 | Mengekspor seluruh data ke format PDF | Admin menekan tombol Ekspor PDF tanpa filter aktif | Klik tombol Ekspor PDF | Browser mengunduh file PDF berisi rekap laporan transaksi dengan format tabel yang rapi dan siap cetak | Sesuai harapan | Berhasil

4 | Mengekspor data yang sudah difilter ke format PDF | Admin menerapkan filter kata kunci terlebih dahulu lalu menekan Ekspor PDF | Filter: Kata Kunci: Daging Ayam, lalu klik Ekspor PDF | File PDF yang diunduh hanya berisi transaksi barang Daging Ayam, sesuai dengan hasil filter di layar | Sesuai harapan | Berhasil

---

##### i. Alur Peringatan Dini di Dashboard

Pengujian alur peringatan dini bertujuan untuk memverifikasi bahwa sistem mampu mendeteksi kondisi persediaan yang berisiko secara otomatis dan menampilkannya sebagai peringatan kepada pengguna di halaman *Dashboard*. Terdapat dua jenis peringatan yang diuji, yaitu peringatan stok kritis yang muncul ketika jumlah stok suatu barang berada pada atau di bawah batas minimum yang telah ditetapkan, serta peringatan mendekati kadaluarsa yang muncul ketika terdapat *batch* stok dengan tanggal kadaluarsa dalam jangka tujuh hari ke depan.

[Tabel Pengujian Alur Peringatan Dini Dashboard]

KOLOM: No | Nama Pengujian | Skenario Uji | Data Input | Hasil yang Diharapkan | Hasil Pengujian | Status

1 | Peringatan stok kritis muncul di Dashboard | Stok suatu barang berkurang hingga berada di bawah atau sama dengan nilai stok minimal yang ditetapkan | Stok Daging Ayam: 3 Kg, Stok Minimal: 5 Kg | Halaman Dashboard menampilkan Daging Ayam pada panel Peringatan Stok Kritis dengan label berwarna merah | Sesuai harapan | Berhasil

2 | Peringatan stok kritis tidak muncul jika stok aman | Stok suatu barang berada di atas nilai stok minimal | Stok Daging Ayam: 20 Kg, Stok Minimal: 5 Kg | Daging Ayam tidak muncul pada panel Peringatan Stok Kritis | Sesuai harapan | Berhasil

3 | Peringatan mendekati kadaluarsa muncul di Dashboard | Terdapat StokBatch aktif dengan tanggal kadaluarsa dalam 7 hari ke depan | Batch Daging Ayam dengan exp. H-3 dari tanggal hari ini | Halaman Dashboard menampilkan Daging Ayam pada panel Peringatan Kadaluarsa dengan label berwarna kuning | Sesuai harapan | Berhasil

4 | Peringatan kadaluarsa tidak muncul jika masih jauh | Semua StokBatch memiliki tanggal kadaluarsa lebih dari 7 hari ke depan | Batch Daging Ayam dengan exp. H-30 dari hari ini | Daging Ayam tidak muncul pada panel Peringatan Kadaluarsa | Sesuai harapan | Berhasil

5 | Panel Dashboard menampilkan pesan aman jika tidak ada peringatan | Semua barang memiliki stok aman dan tidak ada batch yang mendekati kadaluarsa | Semua stok di atas minimal dan exp. > 7 hari | Panel peringatan Dashboard menampilkan pesan Semua Aman | Sesuai harapan | Berhasil
