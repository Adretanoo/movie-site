"""
Django settings for cinemasite project.

Generated by 'django-admin startproject' using Django 5.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""
import os
from dotenv import load_dotenv
from pathlib import Path

menu = [
    {'title': 'Статистика', 'url_name': 'statistics', 'group': ['statistics','statistics_users'], 'icon': 'fa-chart-line'},
    {'title': 'Баннера/Слайдеры', 'url_name': 'banners-sliders', 'group': ['banners-sliders', 'banners-sliders-add'],
     'icon': 'fa-image'},
    {'title': 'Фильмы', 'url_name': 'movies', 'group': ['movies', 'movie_add', 'movie_edit'], 'icon': 'fa-film'},
    {'title': 'Кинотеатры', 'url_name': 'cinemas',
     'group': ['cinemas', 'cinemas_add', 'cinemas_edit', 'hall_add', 'hall_edit'], 'icon': 'fa-building'},
    {'title': 'Новости', 'url_name': 'news', 'group': ['news', 'add_news', 'edit_news'], 'icon': 'fa-newspaper'},
    {'title': 'Акции', 'url_name': 'shares', 'group': ['shares', 'add_shares', 'edit_shares'], 'icon': 'fa-tags'},
    {'title': 'Страницы', 'url_name': 'pages',
     'group': ['pages', 'about', 'cafe_bar', 'vip_hall', 'advertising', 'children_room', 'main_page', 'contacts_page',
               'new_page_add', 'new_page_edit'], 'icon': 'fa-file-alt'},
    {'title': 'Пользователи', 'url_name': 'users', 'group': ['users','user_edit'], 'icon': 'fa-users'},
    {'title': 'Рассылка', 'url_name': 'mailing', 'group': ['mailing'], 'icon': 'fa-envelope'},
]

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s&0@f4*)#!5ce59rn7@ukif0h(8(=&og9q49)r*c)4l7im186g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
INTERNAL_IPS = ["127.0.0.1"]
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'ajax_datatable',
    'widget_tweaks',
    'modeltranslation',
    "debug_toolbar",
    'adminlte.apps.AdminlteConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'cinemasite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cinemasite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'ru-Ru'

LANGUAGES = [
    ('uk', 'Ukrainian'),
    ('ru', 'Russian'),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
