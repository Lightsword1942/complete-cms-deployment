# -*- coding: utf-8 -*-

DEBUG = %(django_debug)s
TEMPLATE_DEBUG = DEBUG

#staticfiles

STATIC_ROOT = "/home/%(user)s/static"
STATIC_URL = "/static/"

MEDIA_ROOT = '%%s/media' %% STATIC_ROOT
MEDIA_URL = '%%smedia/' %% STATIC_URL

DEFAULT_FROM_EMAIL = '%(project_name)s@%(project_name)s.com'

ADMINS = (
    ('Me','me@%(project_name)s.com'),
)
MNAGERS = (
    ('You','you@%(project_name)s.com'),
)
ADMIN_MEDIA_PREFIX = '%%sadmin/' %% STATIC_URL

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '%(db_name)s',                      # Or path to database file if using sqlite3.
        'USER': '%(db_user)s',                      # Not used with sqlite3.
        'PASSWORD': '%(db_password)s',                  # Not used with sqlite3.
        'HOST': '%(db_host)s',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "%(db_user)s" # own settings later
BROKER_PASSWORD = "%(db_password)s"
BROKER_VHOST = "%(db_name)s"

CELERYD_CONCURRENCY = 10
CELERYD_LOG_FILE = "celeryd.log"
#CELERYD_LOG_LEVEL = "INFO"

CACHE_BACKEND = 'memcached://127.0.0.1:%(memcached_port)s/'
CACHE_MIDDLEWARE_SECONDS = 60*5
CACHE_MIDDLEWARE_KEY_PREFIX = '%(project_name)s.'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

HAYSTACK_SOLR_URL = 'http://localhost:8080/solr/%(solr_core)s'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'me@%(project_name)s.com'
EMAIL_HOST_PASSWORD = '%(db_password)s'
EMAIL_USE_TLS = True


%(extra_settings)s
