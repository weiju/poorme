# production settings
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'poopreporter',
        'USER': 'dj_ango',
        'PASSWORD': 'django',
        'HOST': '',
        'PORT': '',
    }
}

STATIC_ROOT = '/var/www/static/'

STATICFILES_DIRS = (
    '/var/www/dookiedj/static',
)

TEMPLATE_DIRS = (
    '/var/www/dookiedj/templates',
)
