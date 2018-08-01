# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

# import django

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "d!j3s!7oap@a-&pymrh32xlxm8p@g%5h^ma=3tbyib2b=d3t1="

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django_ordered_field",

    "tests.lists",
    "tests.multi_collection",
    "tests.ordered_table",
    "tests.multi_order",
    "tests.inheritance_with_parent_link_tester",
    "tests.inheritance",
    "tests.abstract_model",
    "tests.proxy_model",
    "tests.many_to_many"
]
argh
SITE_ID = 1

MIDDLEWARE = ()


"""LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True"""


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(funcName)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'debug_log_file':{
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'debug.log',
            'maxBytes': 1024*1024*5,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['debug_log_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['debug_log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        '': {
            'handlers': ['debug_log_file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
