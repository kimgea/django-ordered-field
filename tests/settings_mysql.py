from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_ordered_field',
        'USER': 'django_ordered_field',
        'PASSWORD': 'django_ordered_field',
    }
}

LOGGING['handlers']['debug_log_file']['formatter'] = 'simple'
