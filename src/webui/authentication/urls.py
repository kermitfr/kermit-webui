'''
Created on Sep 20, 2011

@author: mmornati
'''
from webui import settings
from django.conf.urls.defaults import patterns, include
import logging

logger = logging.getLogger(__name__)

#TODO: Refactor making it dynamic
auth_method = settings.auth_method
if auth_method and auth_method == 'saml2':
    urlpatterns = patterns('',
        (r'^saml2/', include('djangosaml2.urls')),
        (r'^saml/', include('djangosaml2.urls')),
    )
else:
    urlpatterns = patterns('',
    )
    logger.info("Default Authentication Method")
    
