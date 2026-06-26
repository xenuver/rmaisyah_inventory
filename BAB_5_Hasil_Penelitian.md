# BAB 5 HASIL PENELITIAN

## 5.1 Perancangan dan Pengembangan

Tahap perancangan dan pengembangan sistem informasi persediaan pada Rumah Makan Aisyah Ngabang dilaksanakan dengan menggunakan metode Rapid Application Development (RAD). Metode RAD dipilih karena mampu menghasilkan sistem yang berkualitas dalam waktu yang relatif singkat melalui siklus pengembangan yang cepat dan melibatkan umpan balik dari pengguna secara berkelanjutan. Proses pengembangan dalam penelitian ini terbagi ke dalam empat fase utama, yaitu Fase Perencanaan Syarat, Fase User Design, Fase Rapid Construction, dan Fase Cutover.

---

### 5.1.1 Fase Perencanaan Syarat

Fase perencanaan syarat merupakan tahapan awal dalam metode RAD yang bertujuan untuk mengidentifikasi dan memprioritaskan seluruh kebutuhan sistem secara terstruktur. Tahapan ini dilaksanakan melalui pertemuan langsung dengan pemilik Rumah Makan Aisyah Ngabang, yaitu Ibu Kusmiati, serta observasi langsung terhadap proses pengelolaan persediaan bahan baku yang sedang berjalan. Hasil dari fase ini berupa rumusan kebutuhan fungsional dan kebutuhan non-fungsional yang menjadi fondasi utama dalam pengembangan sistem.

#### 5.1.1.1 Kebutuhan Fungsional

Kebutuhan fungsional mencakup berbagai layanan atau fungsi yang harus disediakan oleh sistem agar dapat berjalan sesuai tujuan pengembangannya. Berdasarkan hasil analisis kebutuhan yang dilakukan, kebutuhan fungsional sistem dirumuskan sebagai berikut.

Sistem harus menyediakan halaman Dashboard yang menampilkan ringkasan kondisi persediaan secara real-time, mencakup jumlah barang dengan stok kritis, jumlah bahan baku yang mendekati masa kadaluarsa dalam 7 hari ke depan, rekaman aktivitas transaksi terbaru, serta visualisasi grafik distribusi stok per kategori dan tren pergerakan barang masuk dan keluar.

Sistem harus menyediakan modul pengelolaan data master yang memungkinkan pengguna melakukan operasi tambah, ubah, dan hapus terhadap data Barang, Kategori, dan Satuan melalui antarmuka formulir yang muncul tanpa perlu memuat ulang seluruh halaman.

Sistem harus mampu mencatat transaksi Barang Masuk beserta informasi jumlah, identitas pemasok, dan tanggal kadaluarsa untuk setiap kelompok penerimaan barang yang disebut batch.

Sistem harus mampu mencatat transaksi Barang Keluar beserta alasan pengeluaran (Pemakaian Dapur, Rusak, Kadaluarsa, atau Lainnya) dan melakukan validasi kecukupan stok secara otomatis sebelum transaksi disimpan.

Sistem harus menerapkan logika First-In First-Out (FIFO) berbasis batch pada setiap pencatatan Barang Keluar, yaitu dengan memotong stok dari batch yang memiliki tanggal kadaluarsa paling awal terlebih dahulu. Apabila stok satu batch telah habis, sistem secara otomatis melanjutkan pemotongan ke batch berikutnya dalam urutan.

Sistem harus menyediakan modul Buku Besar yang menyajikan riwayat seluruh transaksi masuk dan keluar secara kronologis, dilengkapi dengan fitur penyaringan berdasarkan rentang tanggal dan jenis transaksi, serta fitur ekspor laporan ke format CSV dan PDF.

Sistem harus menerapkan mekanisme autentikasi pengguna sehingga seluruh halaman dan fitur hanya dapat diakses setelah pengguna melakukan login terlebih dahulu.

Sistem harus memberikan notifikasi peringatan dini secara otomatis pada halaman Dashboard ketika stok suatu barang mencapai batas stok minimal dan ketika terdapat bahan baku yang memasuki periode tujuh hari sebelum tanggal kadaluarsa.

Sistem harus secara otomatis membuat catatan transaksi Barang Masuk pertama sebagai Stok Awal ketika pengguna mendaftarkan barang baru dengan nilai stok awal lebih dari nol.

#### 5.1.1.2 Kebutuhan Non-Fungsional

Kebutuhan non-fungsional mendefinisikan standar kualitas dan batasan operasional yang harus dipenuhi oleh sistem di luar aspek fungsional utamanya.

**Pengembangan Platform Persediaan**

Platform dibangun menggunakan bahasa pemrograman Python dengan framework Django sebagai tulang punggung logika sistem di sisi server. Bahasa lainnya yang digunakan adalah HTML dan CSS untuk membangun antarmuka yang ditampilkan kepada pengguna, serta JavaScript untuk menghadirkan interaktivitas pada halaman. Pengelolaan data menggunakan sistem manajemen basis data PostgreSQL.

**Kebutuhan Perangkat Lunak**

Perangkat lunak merupakan komponen penting dalam mendukung keberhasilan jalannya sebuah sistem. Terdapat beberapa perangkat lunak yang digunakan dalam pembuatan sistem informasi persediaan ini, sebagaimana ditunjukkan pada Tabel 5.1 berikut.

**Tabel 5.1 Kebutuhan Perangkat Lunak**

| No | Jenis Software | Software yang Digunakan |
|----|----------------|-------------------------|
| 1  | Bahasa Pemrograman | Python 3.x, HTML, CSS, JavaScript |
| 2  | Framework Backend | Django 5.0 |
| 3  | Database | PostgreSQL |
| 4  | Pustaka Pembuatan PDF | xhtml2pdf |
| 5  | Browser | Google Chrome dan Microsoft Edge |
| 6  | Sistem Operasi | Windows 11 |
| 7  | Text Editor | Visual Studio Code |

---

### 5.1.2 Fase User Design

Fase User Design merupakan tahap di mana peneliti merancang arsitektur teknis dan struktur sistem secara menyeluruh sebagai panduan implementasi. Fase ini menghasilkan rancangan arsitektur sistem persediaan serta rancangan basis data yang menjadi cetak biru pembangunan sistem.

#### 5.1.2.1 Arsitektur Sistem Persediaan

Sistem informasi persediaan pada Rumah Makan Aisyah Ngabang dibangun menggunakan arsitektur monolitik berbasis pola perancangan MVT (Model-View-Template), yang merupakan adaptasi khas dari framework Django. Arsitektur ini membagi sistem menjadi tiga lapisan yang bekerja secara terpadu, yaitu Model untuk pengelolaan data dan logika bisnis, View untuk penanganan permintaan pengguna, dan Template untuk tampilan antarmuka. Pendekatan ini dipilih karena kesesuaiannya dengan skala dan kompleksitas sistem yang dikembangkan, serta kemudahan pengelolaan kode dalam satu basis proyek yang terpadu.

Secara operasional, seluruh konten halaman diproses dan dihasilkan di sisi server sebelum dikirimkan ke peramban pengguna. Untuk meningkatkan responsivitas antarmuka, sistem menggunakan teknologi yang memungkinkan pembaruan konten halaman secara parsial tanpa perlu memuat ulang seluruh halaman. Dengan pendekatan ini, operasi seperti membuka formulir tambah data atau memperbarui tabel dapat dilakukan secara instan sehingga pengalaman pengguna menjadi lebih cepat dan nyaman.

Komponen-komponen utama dalam arsitektur sistem ini adalah sebagai berikut.

**Model** merupakan lapisan yang bertanggung jawab atas definisi struktur data dan logika bisnis. Model berinteraksi langsung dengan basis data PostgreSQL. Model-model utama dalam sistem ini mencakup Barang, Kategori, Satuan, StokBatch, TransaksiBaru (Barang Masuk), dan TransaksiKeluar (Barang Keluar).

**View** merupakan lapisan yang berperan sebagai pengendali dalam menangani permintaan dari pengguna. Sistem menggunakan Class-Based Views (CBV) dengan perlindungan login pada setiap halaman, memastikan hanya pengguna yang telah terautentikasi yang dapat mengakses sistem.

**Template** merupakan lapisan yang bertanggung jawab atas tampilan antarmuka pengguna. Template HTML menggunakan sistem pewarisan sehingga tata letak dasar seperti header, navigasi, dan footer cukup didefinisikan sekali dan digunakan secara konsisten di seluruh halaman.

**Basis Data (PostgreSQL)** merupakan sistem manajemen basis data relasional yang menyimpan seluruh data persediaan secara permanen dan terstruktur.

#### 5.1.2.2 Rancangan Basis Data

Rancangan basis data sistem informasi persediaan ini terdiri dari enam tabel utama yang saling berelasi untuk merepresentasikan entitas dan proses bisnis pengelolaan stok bahan baku. Proses perancangan dimulai dari tahapan normalisasi hingga penyusunan spesifikasi tabel secara mendetail.

**Normalisasi**

Normalisasi adalah proses mengubah relasi menjadi bentuk normal untuk menghilangkan anomali data dan redundansi. Proses ini dilakukan dari bentuk tidak normal (UNF) hingga mencapai Bentuk Normal Ketiga (3NF). Berikut adalah tahapan normalisasi yang diterapkan pada struktur data sistem informasi persediaan Rumah Makan Aisyah Ngabang.

**UNF (Bentuk Tidak Normal)**

```
id_barang + nama_barang + deskripsi_barang + stok_saat_ini + stok_minimal +
nama_kategori + deskripsi_kategori + nama_satuan + singkatan_satuan +
id_batch + jumlah_awal_batch + jumlah_sekarang_batch + expired_date_batch +
supplier_batch + tanggal_batch_dibuat + id_transaksi_masuk + jumlah_masuk +
supplier_masuk + expired_date_masuk + keterangan_masuk + tanggal_masuk +
id_transaksi_keluar + jumlah_keluar + alasan_keluar + keterangan_keluar + tanggal_keluar
```

**1NF (Bentuk Normal Pertama)**

Pada tahap ini, setiap kelompok data yang berulang dipisahkan menjadi tabel tersendiri sehingga setiap baris hanya memuat satu nilai per kolom.

```
tb_barang          = id_barang + nama_barang + deskripsi_barang + stok_saat_ini +
                     stok_minimal + nama_kategori + deskripsi_kategori +
                     nama_satuan + singkatan_satuan

tb_stokbatch       = id_batch + id_barang + jumlah_awal_batch + jumlah_sekarang_batch + expired_date_batch + supplier_batch + tanggal_batch_dibuat

tb_transaksi_masuk = id_transaksi_masuk + id_barang + jumlah_masuk + supplier_masuk + expired_date_masuk + keterangan_masuk + tanggal_masuk

tb_transaksi_keluar = id_transaksi_keluar + id_barang + jumlah_keluar + alasan_keluar + keterangan_keluar + tanggal_keluar
```

**2NF (Bentuk Normal Kedua)**

Atribut yang tidak bergantung penuh pada kunci primer dipisahkan ke tabel referensi tersendiri, sehingga redundansi data dihilangkan.

```
tb_kategori         = id_kategori + nama_kategori + deskripsi_kategori
tb_satuan           = id_satuan + nama_satuan + singkatan_satuan
tb_barang           = id_barang + nama_barang + deskripsi_barang + stok_saat_ini + stok_minimal
tb_stokbatch        = id_batch + jumlah_awal + jumlah_sekarang + expired_date + supplier + tanggal_dibuat
tb_transaksi_masuk  = id_transaksi_masuk + jumlah + supplier + expired_date + keterangan + tanggal
tb_transaksi_keluar = id_transaksi_keluar + jumlah + alasan + keterangan + tanggal
```

**3NF (Bentuk Normal Ketiga)**

Seluruh atribut non-kunci dipastikan hanya bergantung pada kunci primer, bukan pada atribut non-kunci lainnya, sehingga struktur basis data mencapai bentuk optimal.

```
tb_kategori         = id [PK] + nama_kategori + deskripsi
tb_satuan           = id [PK] + nama_satuan + singkatan
tb_barang           = id [PK] + kategori_id [FK] + satuan_id [FK] + nama_barang +
                      stok_saat_ini + stok_minimal + deskripsi + created_at + updated_at
tb_stokbatch        = id [PK] + barang_id [FK] + jumlah_awal + jumlah_sekarang +
                      expired_date + supplier + created_at
tb_transaksi_masuk  = id [PK] + barang_id [FK] + jumlah + supplier + expired_date +
                      keterangan + tanggal_transaksi
tb_transaksi_keluar = id [PK] + barang_id [FK] + jumlah + alasan + keterangan + tanggal_transaksi
```

**Spesifikasi Tabel Database**

Spesifikasi tabel database bertujuan untuk memberikan gambaran teknis mengenai bagaimana data disimpan dan diorganisasi dalam sistem basis data. Berikut adalah tabel-tabel utama yang terdapat dalam basis data sistem informasi persediaan.

**Tabel Kategori**

Tabel Kategori menyimpan data klasifikasi bahan baku seperti Bahan Pokok, Bumbu, dan Minuman. Tabel ini menjadi referensi utama dalam pengelompokan barang sehingga pencarian dan pelaporan dapat dilakukan berdasarkan jenis bahan.

**Tabel 5.2 Spesifikasi Tabel Kategori**

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|----|------------|-----------|---------|-----------------|---------|
| 1  | id | BIGINTEGER | - | NOT NULL | Auto Increment (PK) |
| 2  | nama_kategori | VARCHAR | 100 | NOT NULL | - |
| 3  | deskripsi | TEXT | - | NULL | NULL |

**Tabel Satuan**

Tabel Satuan menyimpan data satuan ukuran yang digunakan dalam pencatatan jumlah bahan baku, seperti Kilogram (Kg), Liter, atau Pcs. Tabel ini memastikan keseragaman satuan dalam seluruh transaksi yang dicatat di sistem.

**Tabel 5.3 Spesifikasi Tabel Satuan**

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|----|------------|-----------|---------|-----------------|---------|
| 1  | id | BIGINTEGER | - | NOT NULL | Auto Increment (PK) |
| 2  | nama_satuan | VARCHAR | 50 | NOT NULL | - |
| 3  | singkatan | VARCHAR | 10 | NULL | NULL |

**Tabel Barang**

Tabel Barang merupakan tabel inti (master data) yang menyimpan data seluruh bahan baku yang dikelola oleh sistem. Tabel ini berisi informasi stok terkini yang diperbarui secara otomatis setiap kali terjadi transaksi masuk atau keluar, serta batas stok minimal sebagai acuan peringatan dini.

**Tabel 5.4 Spesifikasi Tabel Barang**

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|----|------------|-----------|---------|-----------------|---------|
| 1  | id | BIGINTEGER | - | NOT NULL | Auto Increment (PK) |
| 2  | kategori_id | BIGINTEGER | - | NOT NULL | FK to tb_kategori |
| 3  | satuan_id | BIGINTEGER | - | NOT NULL | FK to tb_satuan |
| 4  | nama_barang | VARCHAR | 200 | NOT NULL | - |
| 5  | stok_saat_ini | INTEGER | - | NOT NULL | 0 |
| 6  | stok_minimal | INTEGER | - | NOT NULL | 0 |
| 7  | deskripsi | TEXT | - | NULL | NULL |
| 8  | created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP |
| 9  | updated_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP |

Kolom `kategori_id` dan `satuan_id` menggunakan constraint PROTECT, artinya sistem akan memblokir penghapusan data Kategori atau Satuan yang masih digunakan oleh data Barang. Kolom `stok_saat_ini` tidak diisi secara manual oleh pengguna, melainkan diperbarui secara otomatis oleh sistem setiap kali terjadi pencatatan transaksi.

**Tabel StokBatch**

Tabel StokBatch adalah tabel krusial yang menjadi fondasi penerapan metode FIFO dalam sistem ini. Setiap kali terjadi penerimaan barang, sistem membuat satu record baru di tabel ini untuk merepresentasikan satu kelompok (batch) stok yang diterima. Tabel ini menyimpan informasi jumlah stok sekarang pada setiap batch beserta tanggal kadaluarsanya, sehingga sistem dapat menentukan batch mana yang harus dikeluarkan terlebih dahulu.

**Tabel 5.5 Spesifikasi Tabel StokBatch**

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|----|------------|-----------|---------|-----------------|---------|
| 1  | id | BIGINTEGER | - | NOT NULL | Auto Increment (PK) |
| 2  | barang_id | BIGINTEGER | - | NOT NULL | FK to tb_barang |
| 3  | jumlah_awal | INTEGER | - | NOT NULL | - |
| 4  | jumlah_sekarang | INTEGER | - | NOT NULL | - |
| 5  | expired_date | DATE | - | NULL | NULL |
| 6  | supplier | VARCHAR | 200 | NULL | NULL |
| 7  | created_at | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP |

Kolom `expired_date` bersifat opsional karena tidak semua bahan baku memiliki tanggal kadaluarsa. Kolom `created_at` digunakan sebagai tiebreaker pada logika FIFO: jika dua batch memiliki tanggal kadaluarsa yang sama atau keduanya tidak memiliki tanggal kadaluarsa, maka batch yang lebih lama dibuat akan dikeluarkan terlebih dahulu.

**Tabel Transaksi Barang Masuk**

Tabel Transaksi Barang Masuk berfungsi sebagai catatan log permanen atas setiap penerimaan bahan baku. Setiap record pada tabel ini merepresentasikan satu kejadian penerimaan barang yang secara bersamaan juga memicu pembuatan record baru di tabel StokBatch.

**Tabel 5.6 Spesifikasi Tabel Transaksi Barang Masuk**

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|----|------------|-----------|---------|-----------------|---------|
| 1  | id | BIGINTEGER | - | NOT NULL | Auto Increment (PK) |
| 2  | barang_id | BIGINTEGER | - | NOT NULL | FK to tb_barang |
| 3  | jumlah | INTEGER | - | NOT NULL | - |
| 4  | supplier | VARCHAR | 200 | NULL | NULL |
| 5  | expired_date | DATE | - | NULL | NULL |
| 6  | keterangan | TEXT | - | NULL | NULL |
| 7  | tanggal_transaksi | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP |

Kolom `supplier` hanya disimpan sebagai teks deskriptif sesuai dengan batasan ruang lingkup sistem yang tidak menyediakan modul manajemen pemasok secara khusus. Data ini berfungsi sebagai informasi historis untuk keperluan penelusuran asal-usul bahan baku jika dibutuhkan.

**Tabel Transaksi Barang Keluar**

Tabel Transaksi Barang Keluar berfungsi sebagai catatan log permanen atas setiap pengeluaran bahan baku. Setiap record pada tabel ini memicu sistem untuk menjalankan logika FIFO secara otomatis, yaitu menelusuri dan memotong stok dari batch-batch yang tersedia dimulai dari yang paling dekat masa kadaluarsanya.

**Tabel 5.7 Spesifikasi Tabel Transaksi Barang Keluar**

| No | Nama Kolom | Tipe Data | Panjang | NULL / NOT NULL | Default |
|----|------------|-----------|---------|-----------------|---------|
| 1  | id | BIGINTEGER | - | NOT NULL | Auto Increment (PK) |
| 2  | barang_id | BIGINTEGER | - | NOT NULL | FK to tb_barang |
| 3  | jumlah | INTEGER | - | NOT NULL | - |
| 4  | alasan | VARCHAR | 20 | NOT NULL | - |
| 5  | keterangan | TEXT | - | NULL | NULL |
| 6  | tanggal_transaksi | DATETIME | - | NOT NULL | CURRENT_TIMESTAMP |

Kolom `alasan` menyimpan salah satu dari empat nilai yang telah ditentukan, yaitu: Pemakaian Dapur, Rusak, Kadaluarsa, atau Lainnya. Pilihan alasan yang terstruktur ini memungkinkan sistem menghasilkan laporan yang dapat dianalisis lebih lanjut berdasarkan penyebab pengeluaran barang.

---

### 5.1.3 Fase Rapid Construction

Fase Rapid Construction merupakan tahap implementasi di mana seluruh rancangan yang telah dirumuskan pada fase sebelumnya diwujudkan menjadi kode program yang berfungsi. Pada fase ini, komponen frontend dan backend sistem dikembangkan secara bersamaan dalam kerangka arsitektur MVT Django. Berikut adalah hasil perancangan sistem informasi persediaan Rumah Makan Aisyah Ngabang.

#### 5.1.3.1 Frontend

Komponen frontend mencakup seluruh elemen antarmuka pengguna yang tampil di peramban, mulai dari tata letak halaman, formulir input, tabel data, hingga visualisasi grafis. Halaman frontend dibangun menggunakan template HTML yang diproses oleh mesin template Django, dengan tampilan visual yang diformat menggunakan framework Tailwind CSS. Teknologi JavaScript digunakan untuk menghadirkan interaktivitas dinamis seperti membuka dan menutup formulir serta memperbarui tabel data tanpa memuat ulang seluruh halaman. Selain itu, pustaka Chart.js digunakan untuk merender visualisasi grafik pada halaman Dashboard. Berikut adalah halaman-halaman antarmuka yang berhasil diimplementasikan.

**Halaman Login**

Halaman Login merupakan gerbang utama sistem yang harus dilalui oleh semua pengguna sebelum dapat mengakses halaman manapun. Pengguna diwajibkan memasukkan nama pengguna dan kata sandi yang valid. Jika kredensial tidak sesuai, sistem menampilkan pesan kesalahan dan akses ditolak. Setelah login berhasil, pengguna diarahkan secara otomatis ke halaman Dashboard.

**Halaman Dashboard**

Halaman Dashboard adalah halaman utama yang pertama kali dilihat pengguna setelah login. Halaman ini menyajikan gambaran menyeluruh kondisi persediaan secara real-time melalui beberapa elemen. Kartu ringkasan metrik menampilkan jumlah barang dengan stok kritis dan jumlah bahan baku yang mendekati masa kadaluarsa dalam 7 hari ke depan. Panel notifikasi peringatan dini menampilkan daftar nama barang beserta sisa stok aktualnya. Log aktivitas menampilkan beberapa entri transaksi terakhir secara kronologis. Grafik Doughnut menampilkan proporsi distribusi stok berdasarkan kategori barang, sedangkan grafik Line menampilkan tren jumlah transaksi barang masuk dan keluar dalam beberapa periode terakhir.

**Halaman Daftar Barang, Kategori, dan Satuan**

Ketiga halaman ini menyajikan data master dalam format tabel yang memuat informasi lengkap setiap entitas. Setiap halaman dilengkapi dengan formulir untuk operasi Tambah, Ubah, dan Hapus data. Seluruh formulir terbuka tanpa memuat ulang halaman, dan setelah operasi berhasil, tabel di halaman utama diperbarui secara otomatis.

**Halaman Log Barang Masuk**

Halaman ini menampilkan riwayat seluruh transaksi penerimaan barang secara kronologis. Dilengkapi dengan formulir "Catat Barang Masuk" yang memungkinkan pengguna merekam penerimaan bahan baku baru beserta detail jumlah, nama pemasok, dan tanggal kadaluarsa apabila tersedia.

**Halaman Log Barang Keluar**

Halaman ini menampilkan riwayat seluruh transaksi pengeluaran barang. Dilengkapi dengan formulir "Catat Barang Keluar" yang memungkinkan pengguna merekam pengeluaran bahan baku beserta alasan pengeluarannya dari pilihan yang telah tersedia.

**Halaman Buku Besar**

Halaman ini menampilkan rekap gabungan seluruh transaksi masuk dan keluar secara kronologis dalam satu tampilan tabel terpadu. Pengguna dapat menyaring data berdasarkan rentang tanggal dan jenis transaksi, serta mengunduh laporan dalam format CSV maupun PDF menggunakan tombol ekspor yang tersedia.

#### 5.1.3.2 Backend

Komponen backend bertanggung jawab atas seluruh logika pemrosesan data, penerapan aturan bisnis, komunikasi dengan basis data, serta penyajian respons kepada antarmuka pengguna. Implementasi backend sistem ini sepenuhnya menggunakan framework Django dengan Python sebagai bahasa pemrogramannya. Berikut adalah komponen-komponen utama yang diimplementasikan pada sisi backend.

**Pengelolaan Model dan Basis Data**

Seluruh entitas basis data diimplementasikan sebagai kelas Model Django. Sistem menggunakan Object-Relational Mapping (ORM) yang memungkinkan interaksi dengan basis data PostgreSQL menggunakan sintaks Python tanpa perlu menulis perintah SQL secara langsung. Validasi tingkat model juga diterapkan untuk memastikan integritas data sebelum disimpan ke basis data.

**Penanganan Permintaan Pengguna**

Logika penanganan permintaan diimplementasikan menggunakan Class-Based Views (CBV), di mana setiap modul fungsional memiliki kelas penanganan tersendiri. Perlindungan autentikasi diterapkan secara konsisten di seluruh modul, memastikan setiap halaman hanya dapat diakses oleh pengguna yang telah melakukan login.

**Logika FIFO (First-In First-Out)**

Logika FIFO merupakan inti dari logika bisnis sistem yang dijalankan secara otomatis setiap kali terjadi pencatatan Barang Keluar. Cara kerjanya adalah sebagai berikut: sistem mengambil seluruh data batch milik barang yang dikeluarkan, lalu mengurutkannya berdasarkan tanggal kadaluarsa yang paling dekat. Sistem kemudian melakukan iterasi pada batch-batch tersebut secara berurutan dan memotong nilai stok sekarang pada setiap batch sesuai jumlah yang dikeluarkan. Pemotongan per batch ini juga dicatat secara rinci dalam tabel BarangKeluarBatch. Apabila satu batch telah habis, sistem secara otomatis melanjutkan pemotongan ke batch berikutnya dalam urutan hingga total jumlah yang dikeluarkan terpenuhi. Setelah semua pemotongan selesai, nilai stok terkini pada data master Barang diperbarui secara otomatis.

**Validasi Kecukupan Stok**

Sebelum transaksi Barang Keluar disimpan, sistem melakukan pengecekan apakah stok yang tersedia mencukupi jumlah yang akan dikeluarkan. Jika tidak mencukupi, sistem menampilkan pesan kesalahan pada formulir di antarmuka pengguna sehingga transaksi tidak dapat disimpan dan data stok di basis data tetap konsisten.

**Logika Peringatan Dini**

Sistem menghitung data peringatan dini secara otomatis setiap kali halaman Dashboard dimuat. Deteksi stok kritis dilakukan dengan membandingkan stok terkini terhadap stok minimal pada setiap barang. Deteksi bahan mendekati kadaluarsa dilakukan dengan mencari data batch yang tanggal kadaluarsanya berada dalam rentang hari ini hingga tujuh hari ke depan dan masih memiliki sisa stok lebih dari nol.

**Ekspor Laporan**

Fitur ekspor laporan ke format CSV diimplementasikan menggunakan modul bawaan Python, yang menghasilkan file teks berformat CSV dengan kolom yang terstruktur. Ekspor ke format PDF diimplementasikan dengan mengonversi template HTML laporan menjadi dokumen PDF yang dapat diunduh oleh pengguna.

**Proteksi Integritas Data**

Sistem memanfaatkan mekanisme perlindungan basis data pada relasi antara Barang dengan Kategori dan Satuan. Mekanisme ini memastikan bahwa upaya menghapus data Kategori atau Satuan yang masih digunakan oleh data Barang akan diblokir secara otomatis. Sistem kemudian menampilkan informasi kesalahan yang mudah dipahami oleh pengguna.

---

### 5.1.4 Fase Cutover

Fase Cutover merupakan tahapan akhir dalam metode RAD yang mencakup persiapan sistem untuk beroperasi di lingkungan nyata. Pada fase ini, pengujian sistem dilaksanakan untuk memastikan seluruh fungsionalitas utama berjalan sesuai dengan spesifikasi yang telah ditetapkan sebelum sistem diserahkan kepada pihak Rumah Makan Aisyah Ngabang untuk digunakan secara operasional. Pengujian yang dilakukan menggunakan metode Black Box Testing, di mana sistem diuji dari perspektif pengguna tanpa memperhatikan struktur kode internal.

---

## 5.2 Demonstrasi

Tahap demonstrasi dilakukan dengan menyimulasikan pengoperasian sistem informasi persediaan yang telah dibangun untuk membuktikan bahwa sistem mampu menyelesaikan permasalahan pengelolaan persediaan yang dihadapi oleh Rumah Makan Aisyah Ngabang. Simulasi ini bertujuan untuk menguji kemampuan sistem dalam mengakomodasi seluruh alur kerja utama, mulai dari pendataan master data, pencatatan transaksi barang masuk dan keluar dengan penerapan logika FIFO, hingga pembuatan laporan buku besar. Seluruh proses demonstrasi dijalankan melalui peramban web menggunakan perangkat laptop.

### 5.2.1 Demonstrasi Halaman Login

Demonstrasi diawali dengan mengakses sistem melalui peramban web. Sistem secara otomatis mengarahkan pengguna ke halaman Login sebagai gerbang keamanan utama. Pengguna memasukkan nama pengguna dan kata sandi yang valid, lalu sistem memvalidasi kredensial tersebut. Setelah autentikasi berhasil, sistem mengarahkan pengguna ke halaman Dashboard. Pada pengujian dengan memasukkan kredensial yang salah, sistem menampilkan pesan kesalahan dan tidak memberikan akses ke halaman manapun, membuktikan bahwa mekanisme perlindungan login berfungsi dengan baik.

### 5.2.2 Demonstrasi Halaman Dashboard

Setelah berhasil login, pengguna disambut oleh halaman Dashboard yang menyajikan gambaran menyeluruh kondisi persediaan secara real-time. Hasil demonstrasi menunjukkan bahwa seluruh elemen Dashboard berfungsi dengan baik. Kartu Ringkasan Metrik menampilkan angka total barang yang berada dalam kondisi stok kritis dan total bahan baku yang mendekati masa kadaluarsa dalam 7 hari ke depan secara akurat sesuai data yang ada di basis data. Panel Peringatan Dini berhasil mendeteksi dan menampilkan daftar nama barang dengan stok kritis beserta sisa stok aktualnya, serta daftar batch bahan baku yang mendekati tanggal kadaluarsa beserta informasi tanggal expired-nya. Log Aktivitas menampilkan beberapa entri transaksi terakhir secara kronologis dengan informasi yang lengkap. Grafik Doughnut dan grafik Line berhasil dirender dengan data yang akurat dan tampilan yang informatif.

### 5.2.3 Demonstrasi Pendataan Master Data

Demonstrasi pengelolaan data master dilaksanakan pada tiga modul, yaitu Kategori, Satuan, dan Barang. Pada setiap modul, alur operasi yang didemonstrasikan mencakup penambahan, pengubahan, dan penghapusan data.

Pada operasi Penambahan Data, pengguna mengklik tombol Tambah sehingga formulir terbuka tanpa memuat ulang halaman. Pengguna mengisi formulir dan menekan tombol simpan. Sistem memvalidasi input, menyimpan data ke basis data, menutup formulir, dan memperbarui tabel secara langsung menampilkan data yang baru ditambahkan.

Pada operasi Pengubahan Data, pengguna mengklik ikon edit pada baris data yang dituju. Formulir terbuka dengan data yang sudah terisi. Pengguna melakukan perubahan dan menyimpan. Sistem memperbarui data di basis data dan menyegarkan tampilan tabel.

Pada operasi Penghapusan Data, sistem menampilkan konfirmasi terlebih dahulu untuk mencegah penghapusan yang tidak disengaja. Sistem menghapus data jika tidak sedang digunakan. Apabila data masih digunakan, sistem menampilkan pesan kesalahan yang informatif.

Saat pengguna mendaftarkan barang baru dengan nilai stok awal lebih dari nol, sistem secara otomatis membuat catatan transaksi Barang Masuk pertama dan data batch pertama tanpa memerlukan tindakan tambahan dari pengguna.

### 5.2.4 Demonstrasi Pencatatan Barang Masuk

Demonstrasi pencatatan Barang Masuk dilakukan dengan mensimulasikan penerimaan bahan baku baru. Pengguna membuka formulir "Catat Barang Masuk", memilih barang dari daftar yang tersedia, mengisi jumlah yang diterima, nama pemasok, dan tanggal kadaluarsa. Setelah formulir disimpan, sistem menjalankan dua operasi secara bersamaan: memperbarui nilai stok terkini pada data master Barang dengan menambahkan jumlah yang baru diterima, dan membuat catatan baru pada tabel StokBatch untuk melacak kelompok stok ini secara terpisah beserta informasi tanggal kadaluarsa dan pemasoknya. Hasil demonstrasi ini membuktikan bahwa sistem mampu mengelola kelompok stok secara independen per batch untuk keperluan penerapan logika FIFO.

### 5.2.5 Demonstrasi Pencatatan Barang Keluar dan Logika FIFO

Demonstrasi pencatatan Barang Keluar merupakan demonstrasi terpenting karena melibatkan logika FIFO yang menjadi keunggulan utama sistem. Untuk keperluan demonstrasi, terlebih dahulu disiapkan sebuah skenario di mana bahan baku "Tepung Terigu" memiliki dua kelompok stok dengan tanggal kadaluarsa yang berbeda, yaitu Batch A sebesar 5 Kg dengan tanggal kadaluarsa 20 Juli 2026 dan Batch B sebesar 10 Kg dengan tanggal kadaluarsa 15 Agustus 2026.

Pengguna membuka formulir "Catat Barang Keluar", memilih Tepung Terigu, mengisi jumlah keluar sebesar 7 Kg, dan memilih alasan "Pemakaian Dapur". Setelah formulir disimpan, sistem menjalankan logika FIFO sebagai berikut. Sistem mengambil seluruh batch Tepung Terigu dan mengurutkannya berdasarkan tanggal kadaluarsa secara menaik, sehingga Batch A berada di urutan pertama. Sistem memotong stok Batch A sebesar 5 Kg sehingga batch tersebut habis. Karena kebutuhan 7 Kg belum terpenuhi dan masih kurang 2 Kg, sistem melanjutkan pemotongan ke Batch B sebesar 2 Kg, sehingga sisa stok Batch B menjadi 8 Kg. Nilai stok terkini pada data master Tepung Terigu diperbarui dari 15 Kg menjadi 8 Kg.

Demonstrasi ini membuktikan bahwa sistem berhasil menerapkan prinsip FIFO secara otomatis, di mana bahan baku dengan masa kadaluarsa terdekat selalu diprioritaskan untuk dikeluarkan terlebih dahulu sehingga risiko kerugian akibat bahan baku kadaluarsa dapat diminimalkan. Pengujian validasi stok juga dilakukan dengan mencoba menginput pengeluaran barang melebihi stok yang tersedia. Sistem berhasil mendeteksi kondisi ini, menampilkan pesan kesalahan pada formulir, dan memblokir penyimpanan transaksi sehingga data stok di basis data tetap konsisten.

### 5.2.6 Demonstrasi Buku Besar dan Ekspor Laporan

Demonstrasi modul Buku Besar dilakukan dengan mengakses halaman Ledger yang menyajikan rekap gabungan seluruh transaksi masuk dan keluar secara kronologis dalam format tabel yang lengkap dan mudah dibaca. Pengguna menggunakan fitur penyaringan untuk menampilkan data berdasarkan rentang tanggal tertentu maupun berdasarkan jenis transaksi, dan tabel berhasil diperbarui sesuai kriteria filter yang dipilih.

Demonstrasi fitur ekspor dilakukan dengan mengklik tombol "Export CSV". Sistem menghasilkan file berformat .csv yang dapat diunduh dan dibuka menggunakan aplikasi spreadsheet seperti Microsoft Excel, dengan kolom-kolom yang terstruktur rapi. Selanjutnya, tombol "Export PDF" menghasilkan dokumen PDF yang memuat tabel rekap transaksi dengan format yang sesuai untuk keperluan dokumentasi dan arsip. Kedua fitur ekspor berhasil menghasilkan dokumen yang lengkap dan tidak terpotong.

### 5.2.7 Evaluasi Hasil Demonstrasi

Berdasarkan seluruh skenario demonstrasi yang telah dilaksanakan, sistem informasi persediaan pada Rumah Makan Aisyah Ngabang terbukti berhasil menjalankan seluruh fungsi yang dirancang. Rangkuman hasil evaluasi demonstrasi disajikan pada Tabel 5.8 berikut.

**Tabel 5.8 Ringkasan Hasil Evaluasi Demonstrasi Sistem**

| No | Fungsi yang Didemonstrasikan | Hasil |
|----|------------------------------|-------|
| 1  | Autentikasi dan kontrol akses halaman | Berhasil — Seluruh halaman terproteksi, diarahkan ke login jika belum terautentikasi |
| 2  | Dashboard real-time (metrik, peringatan dini, grafik) | Berhasil — Data ditampilkan akurat dan grafik dirender dengan benar |
| 3  | Operasi CRUD Data Master via formulir tanpa reload halaman | Berhasil — Formulir terbuka dan menutup tanpa reload, tabel diperbarui otomatis |
| 4  | Proteksi penghapusan data yang masih digunakan | Berhasil — Sistem menampilkan pesan kesalahan dan membatalkan penghapusan |
| 5  | Pencatatan Barang Masuk dan pembuatan StokBatch otomatis | Berhasil — Stok bertambah dan data batch baru berhasil dibuat |
| 6  | Pencatatan Barang Keluar dengan logika FIFO berbasis tanggal kadaluarsa | Berhasil — Sistem memotong stok dari batch dengan tanggal kadaluarsa terdekat lebih dulu |
| 7  | Validasi kecukupan stok pada pencatatan Barang Keluar | Berhasil — Sistem memblokir transaksi dan menampilkan pesan kesalahan yang informatif |
| 8  | Penyaringan dan tampilan Buku Besar | Berhasil — Filter tanggal dan jenis transaksi berfungsi dengan benar |
| 9  | Ekspor laporan ke format CSV | Berhasil — File CSV dapat diunduh dan dibuka dengan kolom yang rapi di spreadsheet |
| 10 | Ekspor laporan ke format PDF | Berhasil — Dokumen PDF terhasilkan dengan tabel yang lengkap dan tidak terpotong |

Hasil evaluasi demonstrasi di atas menunjukkan bahwa seluruh fungsionalitas utama sistem telah berjalan sesuai dengan spesifikasi kebutuhan fungsional yang dirumuskan pada fase perencanaan syarat. Sistem informasi persediaan ini terbukti mampu menjawab permasalahan pengelolaan persediaan manual yang dihadapi oleh Rumah Makan Aisyah Ngabang, khususnya dalam hal otomatisasi pencatatan stok, penerapan metode FIFO untuk manajemen kadaluarsa bahan baku, serta penyediaan informasi persediaan secara real-time yang akurat bagi pihak manajemen.
