"""
Django settings for blogproject project.
"""

from pathlib import Path
import os
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# 🔐 SECURITY
# ==============================

SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-change-this-in-production'
)

DEBUG = config('DEBUG', default=False, cast=bool)

# ==============================
# 🌐 ALLOWED HOSTS
# ==============================

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.onrender.com',   # VERY IMPORTANT for Render
]

# ==============================
# 📦 APPLICATIONS
# ==============================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'blogapp',
]

# ==============================
# ⚙️ MIDDLEWARE
# ==============================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # 🔥 REQUIRED FOR RENDER STATIC FILES
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==============================
# 🔗 URL CONFIG
# ==============================

ROOT_URLCONF = 'blogproject.urls'

# ==============================
# 🧩 TEMPLATES
# ==============================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # 🔥 ADD THIS (important for flexibility)
        'DIRS': [BASE_DIR / "templates"],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blogproject.wsgi.application'

# ==============================
# 🗄️ DATABASE
# ==============================

DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ==============================
# 🔑 PASSWORD VALIDATION
# ==============================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================
# 🌍 INTERNATIONALIZATION
# ==============================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

# ==============================
# 📁 STATIC FILES
# ==============================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 🔥 REQUIRED FOR RENDER
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==============================
# 🖼️ MEDIA FILES
# ==============================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==============================
# 🔢 DEFAULT FIELD
# ==============================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================
# 🔒 CSRF (IMPORTANT FOR RENDER)
# ==============================

CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
]

# ==============================
# 🔐 SECURITY (PRODUCTION SAFE)
# ==============================

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
