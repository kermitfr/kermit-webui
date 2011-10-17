'''
Created on Sep 19, 2011

@author: mmornati
'''
import os
import ConfigParser

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
MAINCONF = SITE_ROOT+'/../../kermit-webui.cfg'
if not os.path.isfile(MAINCONF):
    MAINCONF = '/etc/kermit/kermit-webui.cfg'

CONF = ConfigParser.ConfigParser()
CONF.read(MAINCONF)

BASE_URL=CONF.get('webui', 'base_url')

LOGIN_URL=BASE_URL + "/accounts/login/"
LOGIN_REDIRECT_URL = BASE_URL + "/"
LOGOUT_LINK = ""