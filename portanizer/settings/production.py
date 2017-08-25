from .base import *

# DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'portanizer',
        'USER': 'ded',
        'PASSWORD': get_secret("PASSWORD"),
        'HOST': 'localhost',
        'PORT': '',
    }
}
