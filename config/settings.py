from typing import List, Any

import environ
from celery.schedules import crontab

from apps.exchanges.constants import BTC, USD

ROOT_DIR = (
    environ.Path(__file__) - 2
)  # (project_name/config/settings.py - 2 = project_name/)
APPS_DIR = ROOT_DIR.path("apps")

env = environ.Env()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS", default=["localhost", "0.0.0.0", "127.0.0.1", "*"]
)

DEBUG = env.bool("DJANGO_DEBUG", False)

TIME_ZONE = "UTC"

LANGUAGE_CODE = "en-us"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [ROOT_DIR.path("locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL", default="postgres://rate_task_user:rate_task_pass@postgres:5432/rate_task_db")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"


# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_api_key",
    "drf_yasg",
    "django_celery_beat",
    "django_extensions",
]

LOCAL_APPS = [
    "apps.exchanges"
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATIC_ROOT = str(ROOT_DIR("static"))
STATIC_URL = '/static/'
STATICFILES_DIRS = [str(APPS_DIR.path("static"))]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# celery
CELERY_BROKER_URL = env.str("REDIS_URL", default="redis://redis:6379/0")
CELERY_BEAT_SCHEDULE = {
    "get_exchange_rate": {
        "task": "apps.exchanges.tasks.get_exchange_rates",
        "schedule": crontab(minute=f"*/{env.str('EXCHANGE_RATE_TASK_INTERVAL_MIN', default=60)}"),
        "args": (BTC, USD),
    },
}

# REST_FRAMEWORK
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework_api_key.permissions.HasAPIKey",
    ]
}

# Swagger
# ------------------------------------------------------------------------------
SWAGGER_SETTINGS = {
        "SECURITY_DEFINITIONS": {
            "Api-Key": {"type": "apiKey", "name": "Authorization", "in": "header"}
        }
    }

# Alphavantage API
ALPHAVANTAGE_API_KEY = env.str("ALPHAVANTAGE_API_KEY")
