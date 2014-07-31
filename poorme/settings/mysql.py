# MySQL settings
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'poopreporter',
        'USER': 'dj_ango',
        'PASSWORD': 'django',
        'HOST': 'superfiretruck.com',
        'PORT': '',
    }
}
