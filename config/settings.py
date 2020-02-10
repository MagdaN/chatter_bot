import os

import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    SECRET_KEY = os.environ['SECRET_KEY']
except KeyError:
    raise RuntimeError('No SECRET_KEY in .env')

DEBUG = (os.getenv('DEBUG', 'False').upper() == 'TRUE')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost 127.0.0.1 ::1').split()

INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    # local apps
    'chat',
    # 3rd party apps
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'mptt',
]

if DEBUG:
    INSTALLED_APPS += [
        'django_extensions',
        'debug_toolbar',
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

if DEBUG:
    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ] + MIDDLEWARE

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

try:
    DATABASES = {
        'default': dj_database_url.parse(os.environ['DATABASE']),
    }
except KeyError:
    raise RuntimeError('No DATABASE in .env')

if not DEBUG:
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

REPLIES = {
    'initial': 'How can I help you?',
    'unknown': 'Sorry, I don\'t know what that means.',
    'conclusion': '''This is all I can tell you about this topic.
    Do you have more questions? If yes, how can I help you?'''
}

LOGIC_ADAPTER = os.getenv('LOGIC_ADAPTER', 'chat.logic.NaturalLanguageProcessor')
LOGIC_THRESHOLD = float(os.getenv('LOGIC_THRESHOLD', '0.1'))

NLTK_DATA = os.getenv('NLTK_DATA')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_DIR = os.getenv('LOG_DIR')
if LOG_DIR:
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
            'csv': {
                '()': 'chat.logging.CsvFormatter'
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
                'filename': os.path.join(LOG_DIR, 'error.log'),
                'formatter': 'default'
            },
            'chat_log': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(LOG_DIR, 'chat.log'),
                'formatter': 'name'
            },
            'chat_csv_log': {
                'level': 'WARNING',
                'class': 'logging.FileHandler',
                'filename': os.path.join(LOG_DIR, 'chat.csv'),
                'formatter': 'csv'
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins', 'error_log'],
                'level': 'ERROR',
                'propagate': True
            },
            'chat': {
                'handlers': ['chat_log', 'chat_csv_log'],
                'level': LOG_LEVEL,
                'propagate': False
            }
        }
    }
