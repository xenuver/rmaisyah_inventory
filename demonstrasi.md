## 5.2 Demonstrasi Sistem

Demonstrasi sistem dilakukan untuk memperlihatkan hasil akhir pembangunan sistem informasi persediaan bahan baku berbasis web di Rumah Makan Aisyah Ngabang. Sistem ini diakses melalui peramban web dan terdiri atas beberapa modul yang saling terintegrasi, mencakup autentikasi pengguna, pengelolaan data master, pencatatan transaksi persediaan, serta pelaporan. Seluruh fitur didemonstrasikan secara berurutan sesuai alur penggunaan nyata di lapangan.

Akses ke sistem dimulai melalui halaman Login yang mengharuskan pengguna memasukkan username dan password yang telah terdaftar. Setelah autentikasi berhasil, pengguna diarahkan ke halaman Dashboard yang menampilkan kondisi persediaan secara real-time melalui kartu statistik, grafik pergerakan stok 14 hari terakhir, grafik distribusi stok per kategori, serta panel peringatan otomatis untuk barang dengan stok kritis maupun yang mendekati tanggal kadaluarsa. Fitur peringatan dini ini memungkinkan pengelola mengetahui kondisi persediaan yang memerlukan tindakan segera tanpa harus memeriksa data secara manual.

Pengelolaan data referensi dilakukan melalui tiga modul, yaitu Data Barang, Data Kategori, dan Data Satuan. Modul-modul ini memungkinkan pengguna untuk menambah, mengubah, dan menghapus data master yang menjadi acuan di seluruh proses pencatatan transaksi. Pencatatan transaksi harian dilakukan melalui modul Catat Barang Masuk dan Catat Barang Keluar. Pada saat barang masuk dicatat, sistem secara otomatis menambah total stok dan menyimpan informasi batch penerimaan berikut tanggal kadaluarsanya. Pada saat barang keluar dicatat, sistem menerapkan algoritma First In, First Out (FIFO) dengan memprioritaskan pengurangan stok dari batch yang paling awal kedaluwarsa, sekaligus menolak transaksi apabila jumlah yang diminta melebihi stok yang tersedia.

Seluruh riwayat transaksi dapat ditinjau melalui halaman Log Ledger yang menyajikan buku besar persediaan secara kronologis dan dapat disaring berdasarkan nama barang, rentang tanggal, maupun jenis transaksi. Untuk keperluan pelaporan, sistem menyediakan fitur ekspor data dalam format CSV dan PDF yang hasilnya menyesuaikan dengan filter yang sedang aktif, sehingga laporan untuk periode tertentu dapat dicetak atau disimpan dengan mudah.

---

# BAB 6

# PENUTUP

## 6.1 Kesimpulan

Berdasarkan hasil kajian, perancangan, dan pembangunan sistem informasi persediaan bahan baku di Rumah Makan Aisyah Ngabang, maka dapat diambil kesimpulan sebagai berikut:

a. Metodologi Rapid Application Development (RAD) berhasil diterapkan sebagai kerangka pengembangan sistem informasi persediaan bahan baku yang mencakup empat fase, yaitu Requirements Planning, User Design, Rapid Construction, dan Cutover. Pendekatan ini memungkinkan pengembangan sistem berjalan secara iteratif dan adaptif sesuai dengan kebutuhan nyata Rumah Makan Aisyah Ngabang, sehingga sistem dapat diselesaikan secara sistematis dengan melibatkan pemilik usaha di setiap tahapannya.

b. Sistem informasi persediaan berbasis web yang dibangun menggunakan bahasa pemrograman Python dan kerangka kerja Django ini berhasil mentransformasikan proses pengelolaan persediaan dari yang sebelumnya dilakukan secara manual menggunakan catatan tulis tangan menjadi sebuah sistem yang terdigitalisasi, terpusat, dan dapat diakses kapan saja melalui peramban web. Sistem mencakup modul autentikasi, pengelolaan data master (barang, kategori, satuan), pencatatan transaksi masuk dan keluar, serta pelaporan terintegrasi.

c. Algoritma First In, First Out (FIFO) berhasil diimplementasikan ke dalam mekanisme pencatatan barang keluar melalui konsep StokBatch. Setiap penerimaan barang disimpan sebagai entri batch tersendiri yang memuat jumlah dan tanggal kadaluarsa. Ketika terjadi pengeluaran barang, sistem secara otomatis mengutamakan pengurangan stok dari batch yang memiliki tanggal kadaluarsa paling awal, sehingga risiko pemborosan akibat barang kedaluwarsa sebelum terpakai dapat diminimalisasi.

d. Sistem dilengkapi dengan fitur peringatan dini yang secara otomatis memantau dua kondisi kritis persediaan, yaitu stok yang berada pada atau di bawah batas minimal (stok kritis) dan stok yang tanggal kadaluarsanya akan jatuh dalam tujuh hari ke depan (mendekati kadaluarsa). Kedua kondisi ini ditampilkan secara proaktif pada halaman Dashboard, sehingga pengelola dapat mengambil tindakan pencegahan lebih awal tanpa perlu memeriksa data satu per satu.

e. Fitur pelaporan pada halaman Log Ledger memungkinkan pengelola untuk memantau seluruh riwayat transaksi persediaan secara kronologis dengan dukungan filter berdasarkan nama barang, rentang tanggal, dan jenis transaksi. Tersedianya fitur ekspor laporan dalam format CSV dan PDF memudahkan proses pelaporan kepada pemilik usaha serta penyimpanan arsip data persediaan secara periodik.

## 6.2 Saran

Berdasarkan hasil penelitian dan pengembangan sistem yang telah dilakukan, terdapat beberapa saran yang dapat dijadikan pertimbangan untuk pengembangan lebih lanjut di masa mendatang:

a. Sistem yang telah dibangun saat ini berjalan pada lingkungan lokal (localhost). Untuk dapat dimanfaatkan secara optimal dan diakses dari mana saja, disarankan agar sistem di-deploy ke layanan server atau cloud hosting yang memadai sehingga pengelola dapat mengakses aplikasi secara daring kapan pun dibutuhkan.

b. Fitur peringatan dini pada sistem saat ini bersifat pasif, artinya pengguna harus membuka aplikasi terlebih dahulu untuk melihat notifikasi. Untuk meningkatkan efektivitasnya, disarankan agar dikembangkan mekanisme notifikasi aktif seperti pengiriman peringatan melalui e-mail atau pesan singkat secara otomatis ketika kondisi stok kritis atau mendekati kadaluarsa terdeteksi.

c. Pengembangan sistem ke depannya dapat mempertimbangkan penambahan modul manajemen pemasok (supplier) yang lebih lengkap, termasuk riwayat pembelian per pemasok dan perbandingan harga, sehingga proses pengadaan bahan baku dapat direncanakan dengan lebih terstruktur dan efisien.

d. Antarmuka pengguna sistem yang saat ini dioptimalkan untuk tampilan layar komputer dapat dikembangkan lebih lanjut menjadi aplikasi yang sepenuhnya responsif atau berbasis aplikasi mobile, mengingat pengelola rumah makan yang lebih sering berinteraksi melalui perangkat ponsel dalam kegiatan operasional sehari-hari.
