import os
from django.utils.translation import gettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

if os.getenv('DJANGO_DEBUG'):
    DEBUG = (os.getenv('DJANGO_DEBUG').upper() == 'TRUE')
else:
    DEBUG = False

if os.getenv('DJANGO_ALLOWED_HOSTS'):
    ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split()
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '::1']

INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # local apps
    'chat',
    # 3rd party apps
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'chatterbot.ext.django_chatterbot',
]

if DEBUG:
    INSTALLED_APPS += [
        'django_extensions'
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

if os.getenv('DJANGO_USE_SQLITE'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('DJANGO_PSQL_DBNAME'),
            'USER': os.getenv('DJANGO_PSQL_USER'),
            'PASSWORD': os.getenv('DJANGO_PSQL_PASSWORD'),
            'HOST': os.getenv('DJANGO_PSQL_HOST'),
            'PORT': os.getenv('DJANGO_PSQL_PORT'),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root/')

CHATTERBOT = {
    'name': 'Chat Bot',
    'read_only': True,
    'preprocessors': [
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.convert_to_ascii'
    ],
    'logic_adapters': [
        'chatterbot.logic.BestMatch'
    ],
    'storage_adapter': 'chatterbot.storage.DjangoStorageAdapter'
}

LOGGING_DIR = os.getenv('DJANGO_LOGGING_DIR', 'log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s: %(message)s'
        },
        'name': {
            'format': '[%(asctime)s] %(levelname)s %(name)s: %(message)s'
        },
        'console': {
            'format': '[%(asctime)s] %(message)s'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'error_log': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'error.log'),
            'formatter': 'default'
        },
        'chat_log': {
            'level': 'DEBUG',
            'class':'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'chat.log'),
            'formatter': 'name'
        },
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'django.request': {
            'handlers': ['mail_admins', 'error_log'],
            'level': 'ERROR',
            'propagate': True
        },
        'chat': {
            'handlers': ['chat_log'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False
        }
    }
}
