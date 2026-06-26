# ERD - Sistem Informasi Persediaan Rumah Makan Aisyah Ngabang

Salin kode di bawah ke [dbdiagram.io](https://dbdiagram.io)

```dbml
Table tb_kategori {
  id bigint [pk, increment, not null]
  nama_kategori varchar(100) [not null]
  deskripsi text [null]
}

Table tb_satuan {
  id bigint [pk, increment, not null]
  nama_satuan varchar(50) [not null]
  singkatan varchar(10) [null]
}

Table tb_barang {
  id bigint [pk, increment, not null]
  kategori_id bigint [not null, ref: > tb_kategori.id]
  satuan_id bigint [not null, ref: > tb_satuan.id]
  nama_barang varchar(200) [not null]
  stok_saat_ini decimal(12,2) [not null, default: 0]
  stok_minimum decimal(12,2) [not null, default: 0]
  deskripsi text [null]
  created_at datetime [not null, default: `CURRENT_TIMESTAMP`]
  updated_at datetime [not null, default: `CURRENT_TIMESTAMP`]
}

Table tb_stokbatch {
  id bigint [pk, increment, not null]
  barang_id bigint [not null, ref: > tb_barang.id]
  jumlah_awal decimal(12,2) [not null]
  jumlah_sisa decimal(12,2) [not null]
  expired_date date [null]
  supplier varchar(200) [null]
  created_at datetime [not null, default: `CURRENT_TIMESTAMP`]
}

Table tb_transaksi_masuk {
  id bigint [pk, increment, not null]
  barang_id bigint [not null, ref: > tb_barang.id]
  jumlah decimal(12,2) [not null]
  supplier varchar(200) [null]
  expired_date date [null]
  keterangan text [null]
  tanggal_transaksi datetime [not null, default: `CURRENT_TIMESTAMP`]
}

Table tb_transaksi_keluar {
  id bigint [pk, increment, not null]
  barang_id bigint [not null, ref: > tb_barang.id]
  jumlah decimal(12,2) [not null]
  alasan varchar(20) [not null, note: 'Pemakaian Dapur | Rusak | Kadaluarsa | Lainnya']
  keterangan text [null]
  tanggal_transaksi datetime [not null, default: `CURRENT_TIMESTAMP`]
}
```
