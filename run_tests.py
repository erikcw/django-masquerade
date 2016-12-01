#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner
from importlib import import_module

if __name__ == "__main__":
    settings.configure(
        LOGGING={},
        LOGGING_CONFIG={},
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'masquerade',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'test',
            },
        },
        MIDDLEWARE_CLASSES = [
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
            'masquerade.middleware.MasqueradeMiddleware',
        ],
        ROOT_URLCONF='masquerade.test_urls',
        DEBUG=False,
        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
            },
        ]
    )

    django.setup()

    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['masquerade'])
    sys.exit(bool(failures))
