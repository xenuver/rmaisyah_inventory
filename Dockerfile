# ── Stage 1: Base Python image ──────────────────────────────────────────────
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Entrypoint: migrate, seed (idempotent), then start server
CMD ["sh", "-c", "\
    python manage.py migrate --noinput && \
    python manage.py seed_data --skip-if-exists && \
    python manage.py createsuperuser --noinput || true && \
    gunicorn rmaisyah_inventory.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120\
"]
