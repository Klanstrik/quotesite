import secrets
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = False

ALLOWED_HOSTS = ["killonce.pythonanywhere.com"]

CSRF_TRUSTED_ORIGINS = ["https://killonce.pythonanywhere.com"]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
ROOT_URLCONF = "quotesite.urls"


BASE_DIR = Path(__file__).resolve().parent.parent

# СЕКРЕТНЫЙ КЛЮЧ для локалки
SECRET_KEY = "django-insecure-" + secrets.token_urlsafe(50)

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "django.contrib.humanize",
    "django_htmx",
    "quotes",
]


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
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]  # для локального запуска
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

# --- static files ---
STATIC_URL = "/static/"


#STATICFILES_DIRS = [BASE_DIR / "static"]


# STATIC_ROOT = BASE_DIR / "staticfiles"
