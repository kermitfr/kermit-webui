import os
import django

# calculated paths for django and the site
# used as starting points for various other paths
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
#MEDIA_ROOT = os.path.join(SITE_ROOT, 'assets')
# Django settings for the webui.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': SITE_ROOT + '/../db/sqlite.db',   # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
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
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/var/www/kermit-webui/',

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

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative path
    SITE_ROOT + '/../templates'
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
    'webui.acls_manager',
    #'a7x_wsgroups',
)

FIXTURE_DIRS = (
   '/etc/kermit-webui/fixtures/',
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
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/kermit/kermit-webui.log',
            'maxBytes': '16777216', # 16megabytes
            'formatter': 'verbose'
        },
        'kermit_mcol_log':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/kermit/kermit-mcollective-calls.log',
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
            'level': 'DEBUG',
        },
        'webui.restserver.communication': {
            'handlers': ['kermit_mcol_log'],
            'level': 'DEBUG',
        }
    }
}

BASE_URL=""
LOGIN_URL=BASE_URL + "/accounts/login/"
LOGIN_REDIRECT_URL = '/'
#LOGOUT_LINK = ""

RUBY_REST_BASE_URL="http://127.0.0.1:4567/mcollective/"

CRON_POLLING_FREQUENCY=60

AMQP_RECEIVER_FOLDER='/tmp'


#SAML2 Configuration
#TODO: Refactor creating custom module
#LOGIN_URL="/saml2/login/"
#LOGIN_REDIRECT_URL = '/'
#LOGOUT_LINK = ""
#SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#
#BASEDIR = path.dirname(path.abspath(__file__))
#SAML_CONFIG = {
#    # full path to the xmlsec1 binary programm
#    'xmlsec_binary': '/usr/bin/xmlsec1',
#
#    # your entity id, usually your subdomain plus the url to the metadata view
#    'entityid': 'AutomatixD1',
#    
#    #Added to prevent time not synchro between webui-server and IDP server
#    'timeslack': '5000' ,
#
#    # directory with attribute mapping
#    'attribute_map_dir': path.join(BASEDIR, 'attribute-maps'),
#
#    # this block states what services we provide
#    'service': {
#        # we are just a lonely SP
#        'sp' : {
#            'name': 'Automatix Service Provider',
#            'endpoints': {
#                # url and binding to the assetion consumer service view
#                # do not change the binding or service name
#                'assertion_consumer_service': [
#                    ('http://oxitz1atx02.dktetrix.net/saml/SSO',
#                     saml2.BINDING_HTTP_POST),
#                    ],
#                # url and binding to the single logout service view
#                # do not change the binding or service name
#                'single_logout_service': [
#                    ('http://oxitz1atx02.dktetrix.net/saml/logout',
#                     saml2.BINDING_HTTP_REDIRECT),
#                    ],
#                },
#
#             # attributes that this project need to identify a user
#            'required_attributes': ['uid'],
#
#             # attributes that may be useful to have but not required
#            'optional_attributes': ['eduPersonAffiliation'],
#
#            # in this section the list of IdPs we talk to are defined
#            'idp': {
#                # we do not need a WAYF service since there is
#                # only an IdP defined here. This IdP should be
#                # present in our metadata
#
#                # the keys of this dictionary are entity ids
#                #'https://localhost/simplesaml/saml2/idp/metadata.php': {
#                'idpdecathlon.preprod.org': {
#                    'single_sign_on_service': {
#                        saml2.BINDING_HTTP_REDIRECT: 'https://preprod.idpdecathlon.oxylane.com:9031/idp/SSO.saml2',
#                        },
#                    'single_logout_service': {
#                        saml2.BINDING_HTTP_REDIRECT: 'https://preprod.idpdecathlon.oxylane.com:9031/idp/SLO.saml2',
#                        },
#                    },
#                },
#            },
#        },
#
#    # where the remote metadata is stored
#    'metadata': {
#        'local': [path.join(BASEDIR, 'metadata_example.xml')],
#        },
#
#    # set to 1 to output debugging information
#    'debug': 1,
#
#    # certificate
#    'key_file': path.join(BASEDIR, 'mykey.pem'),  # private part
#    'cert_file': path.join(BASEDIR, 'mycert.pem'),  # public part
#
#    # own metadata settings
#    'contact_person': [
#        {'given_name': 'Test',
#         'sur_name': 'Test',
#         'company': 'Oxylanes',
#         'email_address': 'test@oxylane.com',
#         'contact_type': 'technical'},
#        {'given_name': 'Test2',
#         'sur_name': 'Test2',
#         'company': 'Oxylane',
#         'email_address': 'test2@oxylane.com',
#         'contact_type': 'administrative'},
#        ],
#    # you can set multilanguage information here
#    'organization': {
#        'name': [('Oxylane', 'fr'), ('Oxylane', 'en')],
#        'display_name': [('Oxylane', 'fr'), ('Oxylane', 'en')],
#        'url': [('http://www.oxylane.com', 'fr'), ('http://www.oxylane.com/en', 'en')],
#        },
#    'valid_for': 24,  # how long is our metadata valid
#    }
