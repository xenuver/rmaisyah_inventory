# 🚀 Panduan Deploy ke Coolify — Rumah Makan Aisyah Inventory

Panduan ini menjelaskan cara men-deploy aplikasi **rmaisyah_inventory** ke Coolify menggunakan **Docker Compose buildpack**.

---

## Prasyarat

- Coolify sudah terinstall dan dapat diakses.
- Repository sudah di-push ke GitHub/GitLab/Gitea.
- Server sudah memiliki Docker dan Docker Compose.

---

## Langkah 1 — Buat Project Baru di Coolify

1. Login ke **Coolify Dashboard**.
2. Klik **"New Project"** → beri nama (contoh: `rmaisyah-inventory`).
3. Klik **"New Resource"** → pilih **"Docker Compose"**.

---

## Langkah 2 — Hubungkan Repository

1. Di halaman resource baru, pilih **Source** → pilih koneksi Git yang sudah dikonfigurasi (GitHub/GitLab).
2. Pilih repository **`rmaisyah_inventory`**.
3. Pilih **branch** yang ingin di-deploy (contoh: `master`).
4. Coolify akan mendeteksi `docker-compose.yml` secara otomatis.

---

## Langkah 3 — Konfigurasi Environment Variables

Di tab **"Environment Variables"**, tambahkan variabel-variabel berikut:

| Variable | Contoh Nilai | Keterangan |
|---|---|---|
| `SECRET_KEY` | *(generate random key)* | Django secret key, **wajib diisi** |
| `DEBUG` | `False` | Set `False` di production |
| `ALLOWED_HOSTS` | `yourdomain.com,www.yourdomain.com` | Domain yang diizinkan, **isi sesuai domain Anda** |
| `CSRF_TRUSTED_ORIGINS` | `https://yourdomain.com` | Origin CSRF yang dipercaya, **isi sesuai domain Anda** |
| `DB_NAME` | `rmaisyah_inventory` | Nama database |
| `DB_USER` | `postgres` | Username database |
| `DB_PASSWORD` | *(password kuat)* | Password database, **wajib diisi** |
| `DB_HOST` | `db` | Nama service database (biarkan `db`) |
| `DB_PORT` | `5432` | Port database |
| `DJANGO_SUPERUSER_USERNAME` | `admin` | Username admin pertama |
| `DJANGO_SUPERUSER_PASSWORD` | *(password kuat)* | Password admin, **wajib diisi** |
| `DJANGO_SUPERUSER_EMAIL` | `admin@email.com` | Email admin |
| `PORT` | `8000` | Port aplikasi |

> **💡 Generate SECRET_KEY:**
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

---

## Langkah 4 — Konfigurasi Domain & Proxy

1. Di tab **"Domains"**, tambahkan domain Anda (contoh: `https://inventory.yourdomain.com`).
2. Coolify akan otomatis mengurus SSL certificate via Let's Encrypt.
3. Pastikan DNS sudah mengarah ke IP server Coolify.

---

## Langkah 5 — Build & Deploy

1. Klik **"Deploy"** atau **"Save and Deploy"**.
2. Coolify akan:
   - Build image Docker dari `Dockerfile`.
   - Menjalankan `docker-compose.yml`.
   - Menunggu PostgreSQL sehat (`healthcheck`).
   - Menjalankan `python manage.py migrate`.
   - Menjalankan `python manage.py seed_data --skip-if-exists` (**data tidak akan ditimpa jika sudah ada**).
   - Membuat superuser jika belum ada.
   - Menjalankan Gunicorn sebagai web server.

---

## Perilaku Seed Data

Command `seed_data --skip-if-exists` bersifat **idempotent**:

| Kondisi | Hasil |
|---|---|
| Database kosong (deploy pertama) | Data awal di-seed secara otomatis |
| Data sudah ada (re-deploy / update) | Seed **dilewati**, data existing **tidak ditimpa** |
| Ingin reset data (manual, hati-hati!) | Jalankan `python manage.py seed_data --force` |

---

## Langkah 6 — Verifikasi Deploy

Setelah deploy berhasil:

1. Buka `https://yourdomain.com` — halaman login harus muncul.
2. Login dengan superuser yang dikonfigurasi di env var.
3. Cek admin panel di `https://yourdomain.com/admin/`.
4. Pastikan data kategori, satuan, dan barang sudah tersedia.

---

## Re-Deploy / Update

Setiap kali ada perubahan kode:

1. Push ke branch yang terdaftar di Coolify.
2. Coolify akan otomatis trigger build ulang (jika auto-deploy aktif), **atau** klik manual **"Deploy"**.
3. Data di database **aman** — seed tidak akan menimpa data yang sudah ada.

---

## Troubleshooting

### Container `web` gagal start
- Cek log container di Coolify → tab **"Logs"**.
- Pastikan semua env var wajib sudah diisi (`SECRET_KEY`, `DB_PASSWORD`, dll.).

### Error `CSRF verification failed`
- Pastikan `CSRF_TRUSTED_ORIGINS` sudah diisi dengan domain lengkap beserta protokol, contoh: `https://inventory.yourdomain.com`.

### Error `DisallowedHost`
- Pastikan `ALLOWED_HOSTS` sudah mencakup domain Anda.

### Database tidak bisa terhubung
- Pastikan `DB_HOST` tetap `db` (nama service di docker-compose).
- Pastikan `DB_PASSWORD` sama di env var web dan db.

---

## Struktur File Docker

```
rmaisyah_inventory/
├── Dockerfile              # Build image Django
├── docker-compose.yml      # Orkestrasi service (web + db)
├── .env.example            # Template env var (JANGAN commit .env!)
├── requirements.txt        # Python dependencies (termasuk gunicorn)
└── inventory/
    ├── fixtures/
    │   └── initial_data.json   # Fixture data (opsional, backup)
    └── management/
        └── commands/
            └── seed_data.py    # Idempotent seed command
```
