import os
import django

import imp
from django.conf import global_settings
from utils import CONF
from celery.schedules import crontab

# calculated paths for django and the site
# used as starting points for various other paths
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
#MEDIA_ROOT = os.path.join(SITE_ROOT, 'assets')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': CONF.get('webui-database', 'driver'), # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': CONF.get('webui-database', 'name'),   # Or path to database file if using sqlite3.
        'USER': CONF.get('webui-database', 'user'),    # Not used with sqlite3.
        'PASSWORD': CONF.get('webui-database', 'password'),  # Not used with sqlite3.
        'HOST': CONF.get('webui-database', 'host'),    # Set to empty string for localhost. Not used with sqlite3.
        'PORT': CONF.get('webui-database', 'port'),    # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = None

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''


# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
#ADMIN_MEDIA_PREFIX = '/static/admin/'
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

# Additional locations of static files
#Configuring static file by-exception
if not CONF.get("webui", "static_file_location"):
    static_dir = SITE_ROOT + '/../../static'
else:
    static_dir = CONF.get("webui", "static_file_location")
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    static_dir,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5(r@j&%i0fpx3!qbjvp%s3qhr!8r)!l31(zdfj&3cuf^7_-3r3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
    'guardian.backends.ObjectPermissionBackend',
)

ANONYMOUS_USER_ID = -1

ROOT_URLCONF = 'webui.urls'

#Configuring templates by-exception
if not CONF.get("webui", "templates_location"):
    templates_dir = SITE_ROOT + '/../../templates'
else:
    templates_dir = CONF.get("webui", "templates_location")
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative path
    templates_dir
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'guardian',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.admindocs',
    "djcelery",
    "djkombu",
    'webui.platforms',
    'webui.restserver',
    'webui.django_cron',
    'webui.widgets',
    'webui.defaultop',
    'webui.agent',
    'webui.puppetclasses', 
    'webui.serverstatus',
    'webui.serverdetails',
    'webui.exporter',
    'webui.servicestatus',
    'webui.upload',
    'webui.acls_manager',
    'webui.alerting',
    'webui.chain',
    #'a7x_wsgroups',
)

#Configuring fixtures by-exception
if not CONF.get("webui", "fixtures_location"):
    fixtures_dir = SITE_ROOT + '/../../fixtures/'
else:
    fixtures_dir = CONF.get("webui", "fixtures_location")
FIXTURE_DIRS = (
   fixtures_dir,
)

GRAPPELLI_ADMIN_HEADLINE = CONF.get("webui", "admin.area.title")
GRAPPELLI_ADMIN_TITLE = CONF.get("webui", "admin.area.title")

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'kermit_log_file':{
            'level': CONF.get('webui_logs', 'main.level'),
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': CONF.get('webui_logs', 'main.file'),
            'maxBytes': '16777216', # 16megabytes
            'formatter': 'verbose'
        },
        'kermit_mcol_log':{
            'level': CONF.get('webui_logs', 'calls.level'),
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': CONF.get('webui_logs', 'calls.file'),
            'maxBytes': '16777216', # 16megabytes
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'webui': {
            'handlers': ['console', 'kermit_log_file'],
            'level': CONF.get('webui_logs', 'main.level'),
        },
        'webui.restserver.communication': {
            'handlers': ['kermit_mcol_log'],
            'level': CONF.get('webui_logs', 'calls.level'),
        }
    }
}

BASE_URL=CONF.get('webui', 'base_url')
#LOGIN_URL=BASE_URL + "/accounts/login/"
#LOGIN_REDIRECT_URL = '/'
#LOGOUT_LINK = ""

auth_method=CONF.get('webui', 'authentication')

if auth_method:
    platform_name = 'webui.authentication.' + auth_method + ".settings"
    try :
        conf_module = __import__(platform_name, globals(), locals(), "settings")
        # Load the config settings properties into the local scope.
        for setting in dir(conf_module):
            if setting == setting.upper():
                locals()[setting] = getattr(conf_module, setting)
    except:
        print "DEBUG: No auth module found. Initializing DB?"    
            
else:
    from webui.authentication.default.settings import *
    

RUBY_REST_BASE_URL=CONF.get('webui', 'rest_server_url')
#HTTPLIB TimeOut 10 minutes (seconds)
RUBY_REST_SERVER_TIMEOUT=1200

RUBY_REST_PING_URL=CONF.get('webui', 'rest_server_ping_url')

CRON_POLLING_FREQUENCY=60

AMQP_RECEIVER_INVENTORY_FOLDER=CONF.get('webui', 'amqp_receive_inventory_folder')
AMQP_RECEIVER_LOG_FOLDER=CONF.get('webui', 'amqp_receive_log_folder')

FILTERS_SERVER = CONF.getboolean("webui", "filters.server")
FILTERS_CLASS = CONF.getboolean("webui", "filters.class")

SHOW_SCHEDULER = CONF.getboolean("webui", "show_scheduler")

EMAIL_HOST = CONF.get("webui", "email.host")
EMAIL_PORT = CONF.get("webui", "email.port")
EMAIL_HOST_USER = CONF.get("webui", "email.username")
EMAIL_HOST_PASSWORD = CONF.get("webui", "email.password")
EMAIL_USE_TLS = CONF.getboolean("webui", "email.usetls")

LEVELS_NUMBER = CONF.getint("webui", "levels.number")


import djcelery
djcelery.setup_loader()

#To use directly the django database as a broker (no other tools required)
#With this configuration you can't use celery monitor
#BROKER_TRANSPORT = "django"

#Sample Configuration for Redis
BROKER_TRANSPORT = "redis"
BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis"
CELERY_REDIS_HOST = "127.0.0.1"
CELERY_REDIS_PORT = 6379
CELERY_REDIS_DB = 0

#Sample configuration for mongodb
#CELERY_RESULT_BACKEND = "mongodb"
#CELERY_MONGODB_BACKEND_SETTINGS = {
#    "host": "127.0.0.1",
#    "port": 27017,
#    "database": "celery",
#    "taskmeta_collection": "my_taskmeta" # Collection name to use for task output
#}
#
#BROKER_BACKEND = "mongodb"
#BROKER_HOST = "localhost"
#BROKER_PORT = 27017
#BROKER_USER = ""
#BROKER_PASSWORD = ""
#BROKER_VHOST = "celery"

#Sample Configuration for AMQP transport
#BROKER_HOST = "127.0.0.1"
#BROKER_PORT = 5672
#BROKER_USER = "celery"
#BROKER_PASSWORD = "celerypwd"
#BROKER_VHOST = "mmornati"
#CELERY_RESULT_BACKEND = 'amqp'
#CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True
#CELERYD_NODES="w1"

CELERY_IMPORTS = ("webui", )


CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERYBEAT_SCHEDULE = {
    "runs-server-basic-info-update-every-hour": {
        "task": "webui.serverstatus.tasks.server_basic_info",
        "schedule": crontab(minute=0, hour="*/1"),
        "args": ('CronJob',)
    },
    "runs-inventory-once-a-day": {
        "task": "webui.serverstatus.tasks.server_inventory",
        "schedule": crontab(hour=6, minute=30),
        "args": ('CronJob',)
    }, 
        
#Example to run a ping operation every minute               
#    "runs-cronjob-mco-action": {
#        "task": "webui.restserver.tasks.httpcall",
#        "schedule": crontab(minute="*"),
#        "args": ('no-filter', 'rpc-util', 'ping', None)
#    }, 

#    "runs-update-user-groups-once-a-day": {
#        "task": "webui.serverstatus.tasks.server_inventory",
#        "schedule": crontab(hour=6, minute=30),
#        "args": ('CronJob',)
#    },                   
                       
}