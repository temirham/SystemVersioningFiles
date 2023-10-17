from pathlib import Path

# Dirs:
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = '/static/'
ROOT_URLCONF = 'Soft_Site.urls'
FILES_ROOT = BASE_DIR / 'Files'
MEDIA_ROOT = FILES_ROOT / 'media'
VERSION_STORAGE = FILES_ROOT / 'soft_versions'

# Security:
SECRET_KEY = 'django-insecure-r61aqg3o9a(62#!y2$vcznrz%&0352w_5nb*68t=ad+xx9kxlm'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',           },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',          },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',         },
]

# DRF:
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# Application definition:
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Soft_Loading',
    'Profiles',
    'rest_framework',
    'drf_yasg',
    'el_pagination'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
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
WSGI_APPLICATION = 'Soft_Site.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Databases:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Soft_Site_V1',
        'USER': 'postgres',
        'PASSWORD': 'Root_777',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Localisation:
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Firefox problem fixing:
from mimetypes import add_type
add_type("application/javascript", ".js", True)

