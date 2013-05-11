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

STATIC_ROOT = '/home/weiju/webapps/poorme_static/'

STATICFILES_DIRS = (
    '/home/weiju/webapps/poorme/poorme/static',
)

TEMPLATE_DIRS = (
    '/home/weiju/webapps/poorme/poorme/templates',
)
