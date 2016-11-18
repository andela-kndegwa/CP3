from base_settings import *

from base_settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'zuhura_dev',
        'USER': 'zuhura',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
