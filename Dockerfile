# ── Stage 1: Base Python image ──────────────────────────────────────────────
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
# - libpq-dev    : psycopg (PostgreSQL)
# - gcc g++      : compile C extensions
# - pkg-config   : needed by pycairo, freetype-py
# - libcairo2-dev: pycairo
# - libffi-dev   : cffi / cryptography
# - libssl-dev   : cryptography
# - libxml2-dev libxslt-dev: lxml
# - libjpeg-dev zlib1g-dev libpng-dev: pillow
# - libfreetype6-dev: freetype-py / reportlab
# - curl         : healthcheck / utility
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    g++ \
    pkg-config \
    libcairo2-dev \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libfreetype6-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Expose port
EXPOSE 8000

# Entrypoint runs at container start (env vars available here)
ENTRYPOINT ["sh", "entrypoint.sh"]
