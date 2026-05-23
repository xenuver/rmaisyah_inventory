# Agent Instructions — rmaisyah_inventory

Internal inventory management web app for **Rumah Makan Aisyah Ngabang** (small restaurant in Kalimantan Barat). Tracks ingredient stock, incoming/outgoing goods, reorder alerts, and expiry monitoring.

---

## Tech Stack

| Layer | Tool | Notes |
|-------|------|-------|
| Backend | **Django 6.0** | Python 3.12, venv at `env/` |
| Database | **PostgreSQL** | Configured and running via `psycopg` |
| Templates | Django templates | Server-rendered HTML. No SPA/JS framework. |
| UI/UX | **ui-ux-pro-max** skill | See [SKILL.md](.gemini/skills/ui-ux-pro-max/SKILL.md). Generate design system first, then implement. |
| Styling | **Tailwind CSS** | Tailwind via CDN. Clean, data-dense layout, responsive. |

---

## Quick Start

```powershell
# Activate venv (Windows)
.\env\Scripts\activate

# Install dependencies (including PostgreSQL adapter)
pip install -r requirements.txt

# Run dev server
python manage.py runserver

# Migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

---

## Project Layout

```
rmaisyah_inventory/          ← Django project package (settings, urls, wsgi)
  settings.py                ← DJANGO_SETTINGS_MODULE (PostgreSQL configured)
  urls.py                    ← Root URL conf
dashboard/                   ← App for main analytics and dashboard view
inventory/                   ← App for master data (Barang, Kategori, Satuan)
transactions/                ← App for ledger (BarangMasuk, BarangKeluar, StokBatch)
manage.py                    ← Entry point
env/                         ← Python 3.12 virtualenv (DO NOT commit)
templates/                   ← HTML Templates
```

---

## Database Setup

`settings.py` is configured to use PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rmaisyah_inventory',
        'USER': 'postgres',
        'PASSWORD': 'valen123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## UI/UX Workflow (ui-ux-pro-max Skill)

Before building any frontend page, generate a design system:

```powershell
python .gemini/skills/ui-ux-pro-max/scripts/search.py "restaurant inventory dashboard management" --design-system -p "RM Aisyah Inventory"
```

Key skill rules:
- **No emoji icons** — use SVG icons (Heroicons, Lucide)
- **All clickable elements** must have `cursor-pointer`
- **Test light/dark mode** contrast before delivery
- **Responsive** at 375px, 768px, 1024px, 1440px

---

## App Scope & Boundaries

### Roles
1. **Admin** — Full CRUD on all data, user management, transaction logs. No separation of roles requested. All authenticated administrators can perform all actions.

### Core Features
- **Master Data** — Ingredients (name, category, unit, minimum stock)
- **Barang Masuk** — Incoming goods (creates a `StokBatch` with an expiry date)
- **Barang Keluar** — Outgoing goods (automatically deducts stock from active batches using **FIFO** logic)
- **Reports** — Stock levels, incoming/outgoing by period
- **Reorder Point (ROP) / Stok Minimal** — Auto-alert when stock ≤ minimum stock
- **Expiry Monitoring** — FIFO tracking of perishable items via `StokBatch` and its `tanggal_kadaluarsa`

### Hard Boundaries — DO NOT Build
- No customer-facing features (no e-commerce, no POS, no reservations)
- No automated purchasing — system only **recommends** reorder, user buys manually
- No recipe conversion — stock deductions are manual quantity inputs, not calculated from menu sales

---

## Data Flow (FIFO & Batch Tracking)

1. **Incoming:** Admin inputs `BarangMasuk` → A corresponding `StokBatch` is automatically created with the batch quantity and expiry date → `Barang.stok_saat_ini` (cached stock) increases in real-time.
2. **Outgoing:** Admin inputs `BarangKeluar` → Stock is deducted from `StokBatch` instances matching that item, starting from the oldest/earliest expiring batch (FIFO queue) → `BarangKeluarBatch` junction records are created to audit the deduction → `Barang.stok_saat_ini` decreases.
3. **Delete/Update Safety:** 
   - If a `BarangMasuk` is edited/deleted, the action is blocked if parts of its batch have already been consumed.
   - If a `BarangKeluar` is edited/deleted, the batch deductions are cleanly reverted first, then recalculated (on edit) or deleted (on delete) under `transaction.atomic()`.

---

## Dashboard Components

- **Stat cards:** Total items, critical stock count, near-expiry batch count, today's transactions
- **Charts:** Stock trend (line), category breakdown (doughnut)
- **Alert panel:** Critical stock items + expiring batches (yellow/red)
- **Activity log:** Recent transactions with color badges (green = in, red = out)