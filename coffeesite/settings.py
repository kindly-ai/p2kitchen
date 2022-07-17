""" https://docs.djangoproject.com/en/1.9/ref/settings/ """
import sys

from huey import RedisHuey
from urllib.parse import urlparse
import dj_database_url
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "changeme")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DJANGO_DEBUG", True)

TESTING = any(m in sys.modules for m in ["pytest", "py.test"])

ALLOWED_HOSTS = ["*"] if DEBUG else os.getenv("ALLOWED_HOSTS", "").split(",")

# Application definition
INSTALLED_APPS = [
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
]

INSTALLED_APPS += [
    "p2coffee",
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

ROOT_URLCONF = "coffeesite.urls"

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

WSGI_APPLICATION = "coffeesite.wsgi.application"

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
if os.getenv("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.config()

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
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

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

CORS_ALLOWED_ORIGINS = [
    "https://kitchen.kindly.ai",
    "https://kindly-kitchen.netlify.app",
    "http://localhost:3000",
    "http://localhost:5000",
    "http://localhost:8000",
]

# Huey worker
redis_conntion_args = urlparse(os.environ.get("REDIS_URL", "redis://localhost:6379"))
redis_conntion_args = {
    "host": redis_conntion_args.hostname,
    "port": redis_conntion_args.port,
    "password": redis_conntion_args.password,
}
HUEY = RedisHuey("coffeesite", results=False, immediate=TESTING, **redis_conntion_args)

# Slack
SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#kitchen-dev")


# Brewing settings
BREWTIME_AVG_SECONDS = int(os.getenv("BREWTIME_AVG_SECONDS", "290"))  # 4 min and 50 seconds

try:
    from .local_settings import *
except ImportError:
    pass
