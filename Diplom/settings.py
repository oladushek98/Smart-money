"""
Django settings for Diplom project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECRET_KEY = os.environ.get('SECRET_KEY')
# ROOT_URLCONF = os.environ.get('ROOT_URLCONF')
# DB_PAS = os.environ.get('DB_PASSWORD')
SECRET_KEY = 'q+4jl8a@^trw^t-xm&q39rw20cf68(y^!c!d%x29+ve_m_so8@'
ROOT_URLCONF = 'Diplom.urls'
DB_PAS = 'be4377e4a3a167ff72b6b5ac2a94c9d0f47ce2d285da46deeaa418f4366a7204'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['stlab-diplom.herokuapp.com', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main.apps.MainConfig',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.processors.processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'Diplom.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'smart_money',
    #     'USER': 'postgres',
    #     'PASSWORD': 'Volvoxc90',
    #     'HOST': '127.0.0.1',
    #     'PORT': '5432',
    # }

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd5f6sdus2693jd',
        'USER': 'ghyduqyroquizu',
        'PASSWORD': DB_PAS,
        'HOST': 'ec2-54-75-230-253.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     # {
#     #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     # },
#     # {
#     #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     # },
#     # {
#     #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     # },
#     # {
#     #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     # },
# ]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# REDIS_HOST = 'localhost'
# REDIS_PORT = '6379'
# BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
# BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
# CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'


REDIS_HOST = 'ec2-34-252-60-59.eu-west-1.compute.amazonaws.com'
REDIS_PORT = '25969'
BROKER_URL = 'redis://h:pf697461ec2382692f5fa6554abb7a2603aa564b27854d4bc590b20baa34edc7a@ec2-34-252-60-59.eu-west-1.compute.amazonaws.com:25969'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://h:pf697461ec2382692f5fa6554abb7a2603aa564b27854d4bc590b20baa34edc7a@ec2-34-252-60-59.eu-west-1.compute.amazonaws.com:25969'


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'drakulaxxl3@gmail.com'
EMAIL_HOST_PASSWORD = 'accbfpjkefvzzvtu'
EMAIL_PORT = 587

PYDEVD_USE_FRAME_EVAL = 'NO'

import django_heroku
django_heroku.settings(locals())
