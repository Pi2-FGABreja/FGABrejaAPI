from settings import databases, security, static, apps
from datetime import timedelta
from os import path
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

ROOT_URLCONF = 'settings.urls'
WSGI_APPLICATION = 'settings.wsgi.application'

# Applications
INSTALLED_APPS = apps.INSTALLED_APPS
MIDDLEWARE_CLASSES = apps.MIDDLEWARE_CLASSES

# Security
SECRET_KEY = security.SECRET_KEY
DEBUG = security.DEBUG
ALLOWED_HOSTS = security.ALLOWED_HOSTS
LOGIN_URL = security.LOGIN_URL

# Static files
TEMPLATES = static.TEMPLATES
STATIC_URL = static.STATIC_URL
STATICFILES_DIRS = static.STATICFILES_DIRS

# Database
DATABASES = databases.DATABASES

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# CELERY STUFF
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Sao_Paulo'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
# CELERYBEAT_SCHEDULE_FILENAME = "celery-beat.schedule"
CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'controll_process',
        'schedule': timedelta(seconds=30),
    },
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s - Controlling: %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'controlling': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': path.join(BASE_DIR, 'controlling.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'fga-breja': {
            'handlers': ['controlling'],
            'level': 'INFO',
        },
    }
}
