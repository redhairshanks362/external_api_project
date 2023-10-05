"""
Django settings for externalapiproject project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import environ
from pathlib import Path
from environ import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
env = environ.Env()
env.read_env()
# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = env('SECRET_KEY')
SECRET_KEY = 'django-insecure-dpd^jcq!@&kmwtni3mpz!!^!vnruy3n#4h*fqixx@^ram6lwtf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ["*"] if DEBUG else ['192.168.0.186', '127.0.0.1', '5221-219-91-170-183.ngrok-free.app',
                                             'https://5413-123-201-214-38.ngrok-free.app']
environ.Env.read_env()


# Application definition

def get_env(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error = "set the %s env variable" % var_name
        raise ImproperlyConfigured(error)


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base',
    'speedtest',
    'pickup',
    'tvshow',
    'user',
    'celery',
    'pictures',
    'django_celery_results',
    'django_celery_beat',
    'numbers_api',
    'wordOfTheDay',
    'analytics',
]

# Celery Configuration
#from celery import Celery

#app = Celery('externalapiproject')
#app.config_from_object('django.conf:settings', namespace='CELERY')
#app.autodiscover_tasks()

# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_IMPORTS = {"pickup.tasks",}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'externalapiproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'externalapiproject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# env = environ.Env()
# env.read_env()
# print('env', env)
""" NASA API Key"""
NASA_API_KEY = env('NASA_API_KEY')
NASA_API_KEY2 = 'PQ6avKMSg0FxMd26zWmIQvKf6y4fHd950T8E3QLs'

# NASA_API_KEY = get_env('NASA_API_KEY')
"""URL"""
URL = 'https://api.nasa.gov/planetary/apod'
PICKUP_URL = 'https://api.jcwyt.com/pickup'
PICKUP2_URL = 'https://vinuxd.vercel.app/api/pickup'
TV_SHOW_URL = 'https://quotes.alakhpc.com'
NUMBER_API_URL = 'http://numbersapi.com'
# URL = get_env('URL')
# URL = env('URL')
# PICKUP_URL = env('PICKUP_URL')
# PICKUP_URL2 = env('PICKUP2_URL')

CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
#This djang-db can be changed to redis
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'