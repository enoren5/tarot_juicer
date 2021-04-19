"""
Django settings for tarot_juicer project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

from django.contrib.messages import constants as messages
import os
import django_heroku
from decouple import config
import dj_database_url
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
# tarot!7l=5rh&^(_uug%qd845^^(b40e)bl6kyww$z89f-m#tu=8k&tjuicer
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!

if os.environ.get('DJANGO_DEBUG', '') != 'False':
    # These are testing settings:
    DEBUG = True 
    SECURE_HSTS_SECONDS = 0
    # SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_PRELOAD = False
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    print("\nMode: ", '\033[91m' + 'Not Secure' + '\033[0m', "\n") # Added colored output as red
else:
    # These are prod settings:
    DEBUG = False # Set to `False` for prod when done testing prod (for when the project is finally Live)
    SECURE_HSTS_SECONDS = 7200
    # SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    print("\nMode: ", '\033[92m' + 'Secure !!' + '\033[0m', "\n") # Added colored output as green

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(' ')  if 'ALLOWED_HOSTS' in os.environ else ['*']

ADMIN_PATH = os.environ.get('ADMIN_PATH')+'/' if 'ADMIN_PATH' in os.environ else 'admin/'

# Application definition

INSTALLED_APPS = [
    'essays.apps.EssaysConfig',
    'landings.apps.LandingsConfig',
    'generators.apps.GeneratorsConfig',
    'work_orders.apps.WorkOrdersConfig',
    'accounts.apps.AccountsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tarot_juicer.middlewares.authentication_middleware',
]

ROOT_URLCONF = 'tarot_juicer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tarot_juicer.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# To use AWS Postgres db’s locally run:
# `export DATABASE_URL='postgres://USER:PASSWORD@HOST:PORT/NAME'` 

DATABASES = {}

DATABASES = {
   'default': dj_database_url.config(
       default='sqlite:///'+os.path.join(BASE_DIR, 'db.sqlite3'),
       conn_max_age=600)
   }

print("\nDatabase Config: ", '\033[93m' + str(DATABASES) + '\033[0m', "\n")

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/staticfiles/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'tarot_juicer/static/')
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(STATIC_ROOT, 'img')
MEDIA_URL = 'img/'

django_heroku.settings(locals())
# Because the app is not deployed to a custom domain
if 'OPTIONS' in DATABASES['default']:
  del DATABASES['default']['OPTIONS']['sslmode']

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}