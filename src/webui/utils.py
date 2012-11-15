'''
Created on Oct 25, 2011

@author: mmornati
'''
import os
import ConfigParser
import django
import logging

DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

MAINCONF = '/etc/kermit/kermit-webui.cfg'
if not os.path.isfile(MAINCONF):
    MAINCONF = SITE_ROOT + '/kermit-webui.cfg'

CONF = ConfigParser.ConfigParser()
CONF.read(MAINCONF)

logger = logging.getLogger(__name__);


def read_kermit_version():
    try:
        f = open('/etc/kermit/webui/version.txt', 'r')
        version = f.read()
        return version
    except:
        logger.warn("No version file found in /etc/kermit/webui/version.txt")
        return None