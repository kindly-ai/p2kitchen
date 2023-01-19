""" https://docs.djangoproject.com/en/1.9/ref/settings/ """
import os
import sys

import dj_database_url
from dotenv import load_dotenv
from huey import RedisHuey

load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = os.getenv("SECRET_KEY", "changeme")
DEBUG = os.getenv("DJANGO_DEBUG", True)
TESTING = any(m in sys.modules for m in ["pytest", "py.test"])
ALLOWED_HOSTS = ["*"] if DEBUG else os.getenv("ALLOWED_HOSTS", "").split(",")
# Application definition
INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django_extensions",
    "huey.contrib.djhuey",
    "rest_framework",
    "strawberry.django",
    "corsheaders",
    "channels",
]
INSTALLED_APPS += [
    "p2kitchen",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "p2kitchen.urls"
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
WSGI_APPLICATION = "p2kitchen.wsgi.application"
ASGI_APPLICATION = "p2kitchen.asgi.application"
# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
if os.getenv("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.config()
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
# Internationalization
LANGUAGES = [
    ("en", "English"),
]
LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "en")
TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = os.getenv("STATIC_URL", "/static/")
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
# CORS
CORS_ALLOWED_ORIGINS = [
    "https://kitchen.kindly.ai",
    "https://kindly-kitchen.netlify.app",
    "https://p2kitchen.vercel.app",
    "http://localhost:5173",
    "http://localhost:5000",
    "http://localhost:8000",
]
# Huey
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
HUEY = RedisHuey("p2kitchen", results=False, immediate=TESTING, url=REDIS_URL)
# Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    },
}
# Slack
SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
# Brewing settings
BREWTIME_AVG_SECONDS = int(os.getenv("BREWTIME_AVG_SECONDS", "290"))  # 4 min and 50 seconds

try:
    from .local_settings import *
except ImportError:
    pass
