"""
Django settings for brf project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).absolute().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jz5rd23pcbf#m5w^&noox&mk4hw!67^6r+@a&5ig)ed+om3#5#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

HTML_MINIFY = True
COMPRESS_OFFLINE = False
COMPRESS_ENABLED = COMPRESS_OFFLINE
COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
]

DEFAULT_PAGINATION_NUMBER = 10
CORS_ORIGIN_ALLOW_ALL = False
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '127.0.0.1',
    'buyrealfollows.com',
    'www.buyrealfollows.com',
    'api.buyrealfollows.com',
]

CORS_ORIGIN_WHITELIST = (
    'https://www.nvmservers.com',
    'http://www.nvmservers.com',
    'https://nvmservers.com',
    'http://nvmservers.com',
    'https://digitalpagerank.com',
    'http://digitalpagerank.com',
    'https://www.digitalpagerank.com',
    'http://www.digitalpagerank.com',
    'https://buyrealfollows.com',
    'http://buyrealfollows.com',
    'https://www.buyrealfollows.com',
    'http://buyrealfollows.com',
    'http://localhost:3000',
)
SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",
    "django.contrib.sitemaps",
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    "compressor",
    'django_filters',
    'accounts',
    'vendors',
    'services',
    'orders',
    'payments',
    'ticketing',
    'blog',
    'django_q',
    'ckeditor'
]

LOGGING = {
    'version': 1,
    # Version of logging
    'disable_existing_loggers': False,
    # disable logging
    # Handlers #############################################################
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'dataflair-debug.log',
        },
        ########################################################################
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    # Loggers ####################################################################
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': 300,
    },
}

X_FRAME_OPTIONS = 'ALLOWALL'

ACCESS_CONTROL_ALLOW_CREDENTIALS = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django_user_agents.middleware.UserAgentMiddleware"
]

IPRESTRICT_GEOIP_ENABLED = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER_SUPPORT = 'support@buyrealfollows.com'
EMAIL_HOST_PASSWORD_SUPPORT = 'ooqgfrflucsmdpzr'
EMAIL_HOST_USER_NOREPLY = 'noreply@buyrealfollows.com'
EMAIL_HOST_PASSWORD_NOREPLY = 'cavqpcnmmtkxokfl'

ROOT_URLCONF = 'brf.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (BASE_DIR, 'templates'),
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

Q_CLUSTER = {
    'name': 'brf',
    'workers': 4,
    'recycle': 500,
    'timeout': 300,
    'compress': True,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 1,
    'label': 'Django Q',
    'sync': False,
    'redis': 'redis://127.0.0.1:6379/1'
    # 'redis': {
    #     'host': '127.0.0.1',
    #     'port': 6379,
    #     'db': 1,
    #     'password': None,
    #     'socket_timeout': None,
    #     'charset': 'utf-8',
    #     'errors': 'strict',
    #     'unix_socket_path': None
    # }
}

WSGI_APPLICATION = 'brf.wsgi.application'


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter'
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_URL = "/v1/signin"

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

DEV_STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

STATIC_URL = '/assets/'

# STATIC_ROOT = Path(BASE_DIR, "assets")
# DEV_STATIC_ROOT = Path(BASE_DIR, "static")
# MEDIA_ROOT = Path(BASE_DIR, "media")
#
# STATICFILES_DIRS = (
#     DEV_STATIC_ROOT,
# )

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder"
)