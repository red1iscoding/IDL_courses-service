# Use a slim Python base image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies required by psycopg2 (PostgreSQL driver)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy dependency list and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# (Optional) Collect static files – failure is not fatal for API-only service
RUN python manage.py collectstatic --noinput || echo "No static files to collect"

# Render sets $PORT automatically; fall back to 8000 if not set
CMD gunicorn courses_service.wsgi:application --bind 0.0.0.0:${PORT:-8000}
