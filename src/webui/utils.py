'''
Created on Oct 25, 2011

@author: mmornati
'''
import os
import ConfigParser
import django

DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

MAINCONF = SITE_ROOT+'/kermit-webui.cfg'
if not os.path.isfile(MAINCONF):
    MAINCONF = '/etc/kermit/kermit-webui.cfg'

CONF = ConfigParser.ConfigParser()
CONF.read(MAINCONF)