'''
Created on Nov 3, 2011

@author: mmornati
'''
import logging
from django.shortcuts import render_to_response
from webui import settings
from django.template.context import RequestContext
from webui.servicestatus import utils

logger = logging.getLogger(__name__)

def appdetails(request, appname):
    logger.debug("Application Details for %s" % appname)
    if 'webui.servicestatus' in settings.INSTALLED_APPS:
        service_status = utils.test_services() 
    return render_to_response('platforms/application.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "appname": appname ,"service_status":service_status, 'service_status_url':settings.RUBY_REST_PING_URL}, context_instance=RequestContext(request))
