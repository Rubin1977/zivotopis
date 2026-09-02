# settings_test.py
from .base import *
import os


print("OK – Bežíme v testovacom režime (mysite/settings/test.py)")

SECRET_KEY = "test-secret-key"

DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
    }
}

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
}

TEST_RUNNER = "django.test.runner.DiscoverRunner"


