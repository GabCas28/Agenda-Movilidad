"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 2.2.7.

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
SECRET_KEY = "+(q8r#v#f^5q*ie=a)ejwc=_7_=+f)$h%=oi$2!#xzu&-r1!x$"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "hadoop.ugr.es",
    "150.214.190.198",
    "0.0.0.0",
    "127.0.0.1",
    "localhost",
]

# EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST='smtp.gmail.com'
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_bootstrap_icons",
    "main",
    "accounts",
    "agendas",
    "contacts",
    "importer",
    "mailtemplates",
    "mailsender",
    "django_summernote",
    "django_json_widget",
    "sslserver",
]

ADMINS = (("admin", "admin@admin.com"),)
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "main/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "main.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


# def get_env_value(env_variable):
#     try:
#         return os.environ[env_variable]
#     except KeyError:
#         return None


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": get_env_value("POSTGRES_DB") or "agenda",
#         "USER": get_env_value("POSTGRES_USER") or "agenda",
#         "PASSWORD": get_env_value("POSTGRES_USER") or "agenda",
#         "HOST": get_env_value("POSTGRES_HOST") or "127.0.0.1",
#         "PORT": get_env_value("POSTGRES_PORT") or "5432",
#     }
#     # 'default': {
#     #     'ENGINE': 'django.db.backends.postgresql',
#     #     'NAME': 'postgres',
#     #     'USER': 'postgres',
#     #     'PASSWORD': 'postgres',
#     #     'HOST': 'db',
#     #     'PORT': 5432,
#     # }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "static/"

SITE_ROOT = os.path.dirname("/home/agenda/")
STATICFILES_DIRS = (
    # os.path.join(SITE_ROOT, 'static_files/'),
    os.path.join(BASE_DIR, "static"),
    # "/var/www/static/",
)
STATIC_ROOT = os.path.join(SITE_ROOT, "static/")
# STATIC_ROOT = os.path.join('/home/agenda/', 'static/')

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join("/home/agenda/", "media/")
X_FRAME_OPTIONS = "ALLOWALL"

XS_SHARING_ALLOWED_METHODS = ["POST", "GET", "OPTIONS", "PUT", "DELETE"]

SUMMERNOTE_THEME = "bs5"

SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode, default
    #     # "iframe": True,
    #     # Or, you can set it to `False` to use SummernoteInplaceWidget by default - no iframe mode
    #     # In this case, you have to load Bootstrap/jQuery sources and dependencies manually.
    # Use this when you're already using Bootstrap/jQuery based themes.
    "iframe": False,
    # You can put custom Summernote settings
    "summernote": {
        # Change editor size
        "width": "100%",
    },
    'css': (
        "/static/css/styles.css",
    ),
}

# CSRF_COOKIE_SECURE=True
# CSRF_USE_SESSIONS=True

LOGIN_URL = "/accounts/login"


JSON_EDITOR_JS = "https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/9.2.0/jsoneditor.js"
JSON_EDITOR_CSS = (
    "https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/9.2.0/jsoneditor.css"
)

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
