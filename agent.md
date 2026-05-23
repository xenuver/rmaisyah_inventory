# Agent Instructions — rmaisyah_inventory

Internal inventory management web app for **Rumah Makan Aisyah Ngabang** (small restaurant in Kalimantan Barat). Tracks ingredient stock, incoming/outgoing goods, reorder alerts, and expiry monitoring.

---

## Tech Stack

| Layer | Tool | Notes |
|-------|------|-------|
| Backend | **Django 6.0** | Python 3.12, venv at `env/` |
| Database | **PostgreSQL** | Not yet configured — `settings.py` still has SQLite default. Must switch to `psycopg[binary]` + PostgreSQL before building models. |
| Templates | Django templates | Server-rendered HTML. No SPA/JS framework. |
| UI/UX | **ui-ux-pro-max** skill | See [SKILL.md](.gemini/skills/ui-ux-pro-max/SKILL.md). Generate design system first, then implement. |
| Styling | **Tailwind CSS** | Use Tailwind via CDN for rapid development. Emphasize modern data-dense layouts, clean typography (Inter), smooth hover states (`transition-all`, `hover:-translate-y-0.5`), row highlighting, and glassmorphism where appropriate. |

## Quick Start

```powershell
# Activate venv (Windows)
.\env\Scripts\activate

# Install PostgreSQL adapter (not yet installed)
pip install psycopg[binary]

# Run dev server
python manage.py runserver

# Migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## Project Layout

```
rmaisyah_inventory/          ← Django project package (settings, urls, wsgi)
  settings.py                ← DJANGO_SETTINGS_MODULE
  urls.py                    ← Root URL conf (only /admin/ exists)
manage.py                    ← Entry point
env/                         ← Python 3.12 virtualenv (DO NOT commit)
.gemini/skills/ui-ux-pro-max/  ← UI/UX design skill (searchable DB + scripts)
.kiro/steering/ui-ux-pro-max/  ← Same skill, Kiro format
.opencode/skills/ui-ux-pro-max/ ← Same skill, OpenCode format
```

No Django apps exist yet. No models, no templates, no static files.

## Database Setup (CRITICAL — Must Do First)

`settings.py` currently uses SQLite. Switch to PostgreSQL:

```python
# rmaisyah_inventory/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rmaisyah_inventory',
        'USER': 'postgres',
        'PASSWORD': 'valen123',       # Get from user
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Confirm credentials with the user before writing. Always run `makemigrations` then `migrate` after model changes.

## UI/UX Workflow (ui-ux-pro-max Skill)

Before building any frontend page, generate a design system:

```powershell
python .gemini/skills/ui-ux-pro-max/scripts/search.py "restaurant inventory dashboard management" --design-system -p "RM Aisyah Inventory"
```

For page-specific overrides:
```powershell
python .gemini/skills/ui-ux-pro-max/scripts/search.py "restaurant inventory" --design-system --persist -p "RM Aisyah Inventory" --page "dashboard"
```

Key skill rules:
- **No emoji icons** — use SVG icons (Heroicons, Lucide)
- **All clickable elements** must have `cursor-pointer`
- **Test light/dark mode** contrast before delivery
- **Responsive** at 375px, 768px, 1024px, 1440px
- Run the full Pre-Delivery Checklist in SKILL.md before shipping

## App Scope & Boundaries

### Roles (3 levels)
1. **Admin** — Full CRUD on all data, user management

### Core Features
- **Master Data** — Ingredients (name, category, unit, minimum stock)
- **Barang Masuk** — Incoming goods from suppliers (with finance validation)
- **Barang Keluar** — Outgoing goods (kitchen use, spoilage, expired)
- **Reports** — Stock levels, incoming/outgoing by period
- **Reorder Point (ROP)** — Auto-alert when stock ≤ safety stock
- **Expiry Monitoring** — FIFO alerts for perishable items

### Hard Boundaries — DO NOT Build
- No customer-facing features (no e-commerce, no POS, no reservations)
- No automated purchasing — system only **recommends** reorder, user buys manually
- No recipe conversion — stock deductions are manual quantity inputs, not calculated from menu sales

## Data Flow

- **Incoming:** Admin inputs → stock increases in real-time → reports update → Finance & Owner can view
- **Outgoing:** Admin inputs → stock decreases → if stock ≤ minimum → system flags "Reorder Recommended"

## Dashboard Components

- **Stat cards:** Total items, critical stock count, near-expiry count, today's transactions
- **Charts:** Stock trend (line), category breakdown (doughnut)
- **Alert panel:** Critical stock items + expiry warnings (yellow/red)
- **Activity log:** Recent transactions with color badges (green = in, red = out)

## Conventions

- Language: Indonesian (Bahasa Indonesia) for all UI text, labels, and user-facing content
- Settings module: `rmaisyah_inventory.settings`
- Each major feature should be its own Django app (e.g., `inventory`, `transactions`, `reports`, `accounts`)
- Use Django's built-in auth system — extend with a `role` field or profile model
- Templates directory: set `DIRS` in `TEMPLATES` setting to `[BASE_DIR / 'templates']`
- Static files: `STATICFILES_DIRS = [BASE_DIR / 'static']`