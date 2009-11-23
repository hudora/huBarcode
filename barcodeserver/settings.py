# -*- coding: utf-8 -*-
"""
Settings for Django.

Copyright (c) HUDORA. All rights reserved.
"""

# See http://docs.djangoproject.com/en/dev/ref/settings/ for inspiration

import os
import django

DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

try:
    # company internal defaults
    from cs.global_django_settings import *
except:
    # stupid defaults
    DEBUG = True
    TEMPLATE_LOADERS = ['django.template.loaders.app_directories.load_template_source']
    MIDDLEWARE_CLASSES = []
    INSTALLED_APPS = ['django.contrib.markup']
    TEMPLATE_DIRS = []
    SECRET_KEY = 'invalid'
    ROOT_URLCONF = 'urls'
    LANGUAGE_CODE = 'en-us'
    SITE_ID = 1
    USE_I18N = True
    MEDIA_ROOT = ''
    MEDIA_URL = ''
    ADMIN_MEDIA_PREFIX = '/media/'
    

# for testing
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(SITE_ROOT, 'test.db')

SITE_ID = 1

TEMPLATE_DIRS = (os.path.join(SITE_ROOT, 'generic_templates'), )


TEMPLATE_DEBUG = True
TEMPLATE_STRING_IF_INVALID = "__%s__"

INSTALLED_APPS.extend([
    'piston',
])

ROOT_URLCONF='urls'
