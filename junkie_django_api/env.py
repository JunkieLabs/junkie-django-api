import os
# import sys
import environ
from pathlib import Path
# from corsheaders.defaults import default_methods
from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = list(default_headers) + [
    "my-custom-header",
]


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

ENVIRONMENT = os.environ.get('ENV')

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, f'.env.{ENVIRONMENT}'))


DB_HOST = env.str('DB_HOST')
# print("DB_HOST :", DB_HOST)
DB_REGION = env.str('DB_REGION')
# print("DB_REGION :", DB_REGION)
SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.str('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
CORS_ALLOWED_URL = env.list('CORS_ALLOWED_ORIGINS')
AWS_ACCESS_KEY_ID = env.str("AWS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET")
# LOGGING_LEVEL = DJANGO_LOG_LEVEL
LOGGING_HANDLERS = env.list('LOGGING_HANDLERS')
DJANGO_LOG_LEVEL = env.str('DJANGO_LOG_LEVEL', 'INFO')
DJANGO_LOG_FILE = env.str('DJANGO_LOG_FILE')


if ENVIRONMENT == 'local':
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': DJANGO_LOG_FILE,
                'formatter': 'verbose'
            },
            'console': {
                'class': 'logging.StreamHandler',
            }
        },
        'loggers': {
            'django': {
                'handlers': LOGGING_HANDLERS,
                'propagate': False,
                'level': DJANGO_LOG_LEVEL,
            },
            'app.products': {
                'handlers': ['file'],
                'level': 'DEBUG',
            },
            'app.productionLine': {
                'handlers': ['file'],
                'level': 'DEBUG',
            },
            'app.contactUs': {
                'handlers': ['file'],
                'level': 'DEBUG',
            },
        }
    }