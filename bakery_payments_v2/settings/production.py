from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tbkvvf69frcyehn*qy&4ro82&l1rqx$p=ar6-8maenulkv#y1&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bakery',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
