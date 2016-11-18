import dj_database_url

from base_settings import *


DATABASES = {
    'default': dj_database_url.config()
}
