# settings_test.py
from .base import *
import os

print("OK Bežíme v testovacom režime (mysite/settings/test.py)")


# Ak sa nenačíta z .env, použijeme testovaciu hodnotu
SECRET_KEY = os.getenv("SECRET_KEY", "test-secret-key")

# Použijeme jednoduchú databázu SQLite len pre testy
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
    }
}

# V testoch zapneme DEBUG, nech sa chyby zobrazia priamo
DEBUG = True

# Neposielame žiadne skutočné e-maily počas testovania
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Zrýchlime testy vypnutím heslovania a migrácií (nepovinné, ale rýchlejšie)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Zabezpečí, že testy budú bežať izolovane a rýchlo
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}
