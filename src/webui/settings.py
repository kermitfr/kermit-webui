import os
import django
import ConfigParser
import imp

# calculated paths for django and the site
# used as starting points for various other paths
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
#MEDIA_ROOT = os.path.join(SITE_ROOT, 'assets')

MAINCONF = SITE_ROOT+'/kermit-webui.cfg'
if not os.path.isfile(MAINCONF):
    MAINCONF = '/etc/kermit/kermit-webui.cfg'

CONF = ConfigParser.ConfigParser()
CONF.read(MAINCONF)

# Django settings for the webui.

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
TIME_ZONE = 'America/Chicago'

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
    'django.middleware.csrf.CsrfViewMiddleware',
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
    # Uncomment the next line to enable the admin:
    'guardian',
    'grappelli',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'webui.platforms',
    'webui.django_cron',
    'webui.widgets',
    'webui.defaultop',
    'webui.agent',
    'webui.puppetclasses', 
    'webui.serverstatus',
    'webui.serverdetails',
    'webui.appdeploy',
    'webui.exporter',
    'webui.servicestatus',
)

#Configuring fixtures by-exception
if not CONF.get("webui", "fixtures_location"):
    fixtures_dir = SITE_ROOT + '/../../fixtures/'
else:
    fixtures_dir = CONF.get("webui", "fixtures_location")
FIXTURE_DIRS = (
   fixtures_dir,
)

GRAPPELLI_ADMIN_HEADLINE = 'Kermit Admin Area'
GRAPPELLI_ADMIN_TITLE = 'Kermit Admin Area'

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
        print "WARN: No auth module found. Initializing DB?"    
            
else:
    from webui.authentication.default.settings import *
    

RUBY_REST_BASE_URL=CONF.get('webui', 'rest_server_url')

RUBY_REST_PING_URL=CONF.get('webui', 'rest_server_ping_url')

CRON_POLLING_FREQUENCY=60

AMQP_RECEIVER_FOLDER=CONF.get('webui', 'amqp_receive_folder')

