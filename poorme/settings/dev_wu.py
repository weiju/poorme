# Wei-ju's settings
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

STATICFILES_DIRS = (
    '/home/weiju/StartupWeekend/poorme/static',
)

TEMPLATE_DIRS = (
    '/home/weiju/StartupWeekend/poorme/templates',
)
