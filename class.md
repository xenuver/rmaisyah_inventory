# Class Diagram - Sistem Informasi Persediaan Rumah Makan Aisyah Ngabang

Berikut adalah Class Diagram dari model data yang digunakan dalam sistem, dibuat menggunakan format Mermaid. Anda dapat menyalin blok kode di bawah ini ke [mermaid.live](https://mermaid.live) atau mempratinjaunya di editor yang mendukung Markdown Mermaid.

```mermaid
classDiagram
    direction LR

    class Kategori {
        +BigAuto id
        +String nama
        +Text deskripsi
        +DateTime created_at
    }

    class Satuan {
        +BigAuto id
        +String nama
    }

    class Barang {
        +BigAuto id
        +String nama
        +Integer stok_minimal
        +Integer stok_saat_ini
        +DateTime created_at
        +DateTime updated_at
        +is_stok_kritis() Boolean
        +is_mendekati_kadaluarsa() Boolean
        +save()
    }

    class BarangKeluar {
        +BigAuto id
        +Integer jumlah
        +String alasan
        +Date tanggal
        +Text keterangan
        +DateTime created_at
        +clean()
        +restore_batches()
        +save()
        +delete()
    }

    class BarangMasuk {
        +BigAuto id
        +Integer jumlah
        +String supplier
        +Date tanggal
        +Date tanggal_kadaluarsa
        +Text keterangan
        +DateTime created_at
        +clean()
        +save()
        +delete()
    }

    class BarangKeluarBatch {
        +BigAuto id
        +Integer jumlah
    }

    class StokBatch {
        +BigAuto id
        +Integer jumlah_awal
        +Integer jumlah_sekarang
        +Date tanggal_kadaluarsa
        +DateTime created_at
    }

    %% Relasi antar entitas (Model)
    Kategori "1" -- "*" Barang : memiliki
    Satuan "1" -- "*" Barang : memiliki
    
    Barang "1" -- "*" BarangKeluar : mencatat
    Barang "1" -- "*" BarangMasuk : mencatat
    
    BarangKeluar "1" -- "*" BarangKeluarBatch : memotong (FIFO)
    
    BarangMasuk "1" -- "1" StokBatch : membentuk (OneToOne)
    Barang "1" -- "*" StokBatch : memiliki batch
    
    StokBatch "1" -- "*" BarangKeluarBatch : dipotong
```
