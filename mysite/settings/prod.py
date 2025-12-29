from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.pythonanywhere.com', 'eu.pythonanywhere.com']

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'RastislavRuzback$default',
        'USER': 'RastislavRuzback',
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'RastislavRuzbacky.mysql.eu.pythonanywhere-services.com',
        'PORT': '3306',
    }
}

# Email – produkcia cez Gmail SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

SECURE_SSL_REDIRECT = True
