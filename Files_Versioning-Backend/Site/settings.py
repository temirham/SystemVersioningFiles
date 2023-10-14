from datetime import timedelta
from pathlib import Path
from configparser import ConfigParser


# f-strings to allow using path with ' ':
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / 'logs'
CONFIG = ConfigParser()
CONFIG.read(BASE_DIR / 'config.cfg')

SECRET_KEY = 'django-insecure-76)s%1n$x4m$2gx@6hqlmkuyo!zt-z8clke$+ou*!jam87%je&'
ALLOWED_HOSTS = ['127.0.0.1']
DEBUG = True

ROOT_URLCONF = 'Site.urls'
WSGI_APPLICATION = 'Site.wsgi.application'
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STORAGE_WAIT_TIMEOUT = 30

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'Site',
    'Profiles',
    'FilesVersioning',
    'corsheaders',
    'drf_yasg'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':     CONFIG.get('Postgres DB', 'name'),
        'USER':     CONFIG.get('Postgres DB', 'user'),
        'PASSWORD': CONFIG.get('Postgres DB', 'password'),
        'HOST':     CONFIG.get('Postgres DB', 'host'),
        'PORT':     CONFIG.get('Postgres DB', 'port')
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'formatter': {
            'format': '{levelname} - {asctime} - {module} - {process:d} - {thread:d} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'info.log',
        },
        'errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'errors.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['info', 'errors', 'console'],
            'formatter': 'formatter',
            'level': 'INFO',
            'propagate': False
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.tokens.AccessToken'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'EXCEPTION_HANDLER': 'Site.exceptions.drf_exceptions_handler',
    'DATETIME_FORMAT': "%Y-%m-%d",
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]


# CORS_ORIGIN_WHITELIST = (
#     'http://localhost:3000', # For react front end
#     'http://localhost:8000', # For Django
# )
# CORS_ALLOW_CREDENTIALS: True
#
# CORS_ALLOWED_CREDENTIALS=[
#     'http://localhost:3000',
# ]
# CORS_ALLOW_ALL_ORIGINS=True
# CORS_ALLOWED_ORIGINS_REGEXES = [
#     'http://localhost:3000',
#
# ]

LANGUAGE_CODE = 'en-us'
TIME_ZON = 'UTC'
USE_I18N = True
USE_TZ = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'TOKEN_UPDATE_BLACKLIST_ON_LOGOUT': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'TOKEN_TYPE_CLAIM': 'token_type',
    # 'SLIDING_TOKEN_TYPES': {'refresh'},  # Типы токенов
    'JTI_CLAIM': 'jti',
    #
    # 'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    # 'SLIDING_TOKEN_LIFETIME': timedelta(minutes=0),
    # 'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),

    'BLACKLISTED_TOKENS': {
        'access': 'rest_framework_simplejwt.token_blacklist.models.BlacklistedToken',
        'refresh': 'rest_framework_simplejwt.token_blacklist.models.BlacklistedToken',
    }
}