from django.contrib.messages import constants as messages
import os

from decouple import config
import dj_database_url
from dotenv import load_dotenv
from . import notification
load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# As per the django documentation
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Handle session is not Json Serializable
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

SECRET_KEY = str(os.getenv('SECRET_KEY'))

# For discussion of how and why the following line works and what it does, see Issue #262 on GitHub for this repo
DEBUG = os.getenv("DEBUG", "False") == "True"

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 7200
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    # Added colored output as green
    notification.messages_print('success', 'Secure Mode Enabled: DEBUG MODE IS FALSE')
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_PRELOAD = False
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False

    # Added colored output as red
    notification.messages_print('error', 'Secure Mode Disabled: DEBUG MODE IS TRUE')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(' ')  if 'ALLOWED_HOSTS' in os.environ else ['*']

ADMIN_PATH = os.environ.get('ADMIN_PATH')+'/' if 'ADMIN_PATH' in os.environ else 'admin/'

COOKIE_CONSENT_NAME = "cookie_consent"
COOKIE_CONSENT_MAX_AGE = 31536000  # 1 year

# Matomo PURGED 13 February 2026

# Application definition

INSTALLED_APPS = [
    'essays.apps.EssaysConfig',
    'landings.apps.LandingsConfig',
    'generators.apps.GeneratorsConfig',
    'settings_ui.apps.SettingsUiConfig',
    #'work_orders.apps.WorkOrdersConfig',
    # 'accounts.apps.AccountsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'analytical',
    "django_extensions",
    "widget_tweaks",
    "gateway_defender",
    "cookie_consent",
    "django.contrib.sites",
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
    'cookie_consent.middleware.CleanCookiesMiddleware',
    "django.contrib.sites.middleware.CurrentSiteMiddleware",

    # 'tarot_juicer.middlewares.authentication_middleware',
    # 'tarot_juicer.middlewares.autologout_middleware',
    # 'tarot_juicer.protected_path_middleware.path_protection_middleware',  
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
                'settings_ui.context_processors.site_settings',
            ],
            'libraries': {  # Adding this section should work around the issue.
                'staticfiles': 'django.templatetags.static',
            },
        },
    },
]

WSGI_APPLICATION = 'tarot_juicer.wsgi.application'

# Info for gateway-defender to know which template to render when user is authenticated
GATEWAY_PORTAL_TEMPLATE = "landings/portal.html"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# To use AWS Postgres db’s locally run:
# `export DATABASE_URL='postgres://USER:PASSWORD@HOST:PORT/NAME'`

DATABASES = {}

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600
    )
}

notification.messages_print('warning', 'Database Config: ' + str(DATABASES))

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
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'tarot_juicer/static/')
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(STATIC_ROOT, 'img')
MEDIA_URL = 'img/'


# Because the app is not deployed to a custom domain
if 'OPTIONS' in DATABASES['default']:
  del DATABASES['default']['OPTIONS']['sslmode']

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

LOGIN_REDIRECT_URL = '/portal'

LOGOUT_REDIRECT_URL = '/'

