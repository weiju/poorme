# Kathleen's settings
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/Users/ktuite/Desktop/dookie_django/poopreporter.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

STATICFILES_DIRS = (
    '/Users/ktuite/Desktop/dookie_django/static',
)

TEMPLATE_DIRS = (
    '/Users/ktuite/Desktop/dookie_django/templates',
)
