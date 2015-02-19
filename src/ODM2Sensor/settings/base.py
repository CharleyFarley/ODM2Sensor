"""
Django settings for ODM2Sensor project.

"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, os.pardir)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5#3wtm#z(7iexc$k_wm458%*!t0r9izzl6&wux-toj%p9h=-ud'

ALLOWED_HOSTS = []

APPEND_SLASH = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sensordatainterface',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ODM2Sensor.urls'

LOGIN_REDIRECT_URL = '/home/'

WSGI_APPLICATION = 'ODM2Sensor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'ODM2Sensor/Internal.sqlite3',
    },
    'odm2': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'ODM2Equipment',
        'USER': 'Mario',
        'PASSWORD': 'Aixax0822',
        'HOST': 'MANGO\SQLEXPRESS',
        'PORT': '',

        'OPTIONS': {
            'driver': 'SQL Server Native Client 11.0',
            'host_is_server': True,
        },
    },
}

TEMPLATE_DIRS = [os.path.join(PROJECT_DIR, 'templates')]

# Internationalisation
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True