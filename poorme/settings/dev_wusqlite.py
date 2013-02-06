# Wei-ju's sqlite3 settings
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/weiju/StartupWeekend/poorme/poopreporter.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

STATICFILES_DIRS = (
    '/home/weiju/StartupWeekend/poorme/static',
)

TEMPLATE_DIRS = (
    '/home/weiju/StartupWeekend/poorme/templates',
)
