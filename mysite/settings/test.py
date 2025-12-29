# settings_test.py
from .base import *
import os
import socket

print("OK – Bežíme v testovacom režime (mysite/settings/test.py)")

# Rozlíšime lokálne vs. remote podľa hostname
HOSTNAME = socket.gethostname()

# Lokálne testy → SQLite
if "pythonanywhere" not in HOSTNAME:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'test_db.sqlite3',
        }
    }

# Remote testy → MySQL test DB
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'RastislavRuzback$Rastislav',
            'USER': 'RastislavRuzback',
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': 'RastislavRuzbacky.mysql.eu.pythonanywhere-services.com',
            'PORT': '3306',
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


