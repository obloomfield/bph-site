"""
Django settings for bph project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Ensure logs directory exists.
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

SECRET_KEY = os.environ.get("SECRET_KEY", "FIXME_SECRET_KEY_HERE")

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", None)

RECAPTCHA_SITEKEY = None
RECAPTCHA_SECRETKEY = None

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["localhost", "0.0.0.0"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "impersonate",
    "mathfilters",
    "puzzles",
    "channels",
    "django_eventstream",
    "bph.apps.CustomRoomsConfig",
    "rest_framework",
    "rest_framework.authtoken",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "impersonate.middleware.ImpersonateMiddleware",
    "puzzles.messaging.log_request_middleware",
    "puzzles.context.context_middleware",
]

# redis_url = os.environ.get("REDISCLOUD_URL")

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [{"address": redis_url}],
#         },
#     }
# }

# FROM DEV:
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}

EVENTSTREAM_CHANNELMANAGER_CLASS = "puzzles.messaging.AuthChannelManager"

SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_CACHE_ALIAS = "default"

ROOT_URLCONF = "bph.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "puzzles.context.context_processor",
            ],
        },
    },
]

WSGI_APPLICATION = "bph.wsgi.application"
ASGI_APPLICATION = "bph.asgi.application"


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# Apparently conn_max_age=0 is better for Heroku:
# https://stackoverflow.com/questions/48644208/django-postgresql-heroku-operational-error-fatal-too-many-connections-for-r
# DATABASES = {
#    'default': dj_database_url.config(conn_max_age=0, ssl_require=True),
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "bphdb",
        "USER": "bph",
        "PASSWORD": "puzzle_hunting_is_so_cool",
        "HOST": "localhost",  # '127.0.0.1' probably works also
        "PORT": "5432",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, "static"))
SOLUTION_STATIC_ROOT = os.path.normpath(
    os.path.join(BASE_DIR, "puzzles/templates/solution_bodies")
)
STATICFILES_STORAGE = "bph.storage.CustomStorage"

# Email SMTP information

EMAIL_USE_TLS = True
EMAIL_HOST = "FIXME"
EMAIL_HOST_USER = "FIXME"
EMAIL_HOST_PASSWORD = "FIXME"
EMAIL_PORT = "FIXME"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_SUBJECT_PREFIX = "[FIXME Puzzle Hunt] "

# https://docs.djangoproject.com/en/3.1/topics/logging/

# Loggers and handlers both have a log level; handlers ignore messages at lower
# levels. This is useful because a logger can have multiple handlers with
# different log levels.

# The levels are DEBUG < INFO < WARNING < ERROR < CRITICAL. DEBUG logs a *lot*,
# like exceptions every time a template variable is looked up and missing,
# which happens literally all the time, so that might be a bit too much.

# If you want to log to stdout (e.g. on Heroku), the handler looks as follows:
# {
#     'level': 'INFO',
#     'class': 'logging.StreamHandler',
#     'stream': sys.stdout,
#     'formatter': 'django',
# },

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "django": {
            "format": "%(asctime)s (PID %(process)d) [%(levelname)s] %(module)s %(message)s"
        },
        "puzzles": {
            "format": "%(asctime)s (PID %(process)d) [%(levelname)s] %(name)s %(message)s"
        },
    },
    # FIXME you may want to change the filenames to something like
    # /srv/logs/django.log or similar
    "handlers": {
        "django": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "django",
        },
        "general": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "puzzles",
        },
        "puzzle": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "puzzles",
        },
        "request": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "puzzles",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "django.log"),
            "when": "H",
            "interval": 3,
            "backupCount": 36,
            "formatter": "django",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["django", "file"],
            "level": "INFO",
            "propagate": True,
        },
        "puzzles": {
            "handlers": ["general", "file"],
            "level": "INFO",
            "propagate": True,
        },
        "puzzles.puzzle": {
            "handlers": ["puzzle", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "puzzles.request": {
            "handlers": ["request", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
}

SESSION_COOKIE_HTTPONLY = False

# Google Analytics
GA_CODE = ""

LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "index"
