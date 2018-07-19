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
    "tests.multi_ordered",
    "tests.ordered_table",
]

SITE_ID = 1

MIDDLEWARE = ()


"""LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True"""
