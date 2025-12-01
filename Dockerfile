# Use a lightweight Python image
FROM python:3.12-slim

# Prevent .pyc files, force stdout flushing
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Collect static files (won't break if none)
RUN python manage.py collectstatic --noinput || echo "No static files to collect"

# Expose internal port (Render will still set PORT env var)
EXPOSE 8000

# Start Django with Gunicorn, binding to Render's PORT
CMD ["sh", "-c", "gunicorn courses_service.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
