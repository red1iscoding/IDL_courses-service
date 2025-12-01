"""
Django settings for courses_service project (deployment-ready for Render + local dev).
"""

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-secret-key-change-me"  # OK for local dev, NOT for real production
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "False") == "True"

# Allowed hosts: include localhost + Render domains
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]
# Allow anything extra from env (e.g. your Render URL)
EXTRA_ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "")
if EXTRA_ALLOWED_HOSTS:
    ALLOWED_HOSTS += [h.strip() for h in EXTRA_ALLOWED_HOSTS.split(",") if h.strip()]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "corsheaders",

    # Local apps
    "courses",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # CORS should be as high as possible
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "courses_service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "courses_service.wsgi.application"

# Database
# Local dev: falls back to SQLite
# Render: set DATABASE_URL env var (e.g. postgresql://user:pass@host:port/dbname)
DATABASES = {
    "default": dj_database_url.config(
        default="sqlite:///" + str(BASE_DIR / "db.sqlite3"),
        conn_max_age=600,
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# Render: collectstatic will place files into STATIC_ROOT
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React frontend
    "http://localhost:8000",  # Django dev
    "http://localhost:8080",  # Gateway
]

# Allow extra origins from env if needed (e.g. your deployed frontend)
EXTRA_CORS_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "")
if EXTRA_CORS_ORIGINS:
    CORS_ALLOWED_ORIGINS += [
        o.strip() for o in EXTRA_CORS_ORIGINS.split(",") if o.strip()
    ]

CORS_ALLOW_CREDENTIALS = True

# DRF basic configuration (optional, can be customized)
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
}
