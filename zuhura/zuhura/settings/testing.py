from base_settings import *
# Testing Database for Zuhura
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'testdb'),
        'TEST': {
            'NAME': 'test_zuhura.sqlite3',
        },
    }
}
