'''
Created on Nov 3, 2011

@author: mmornati
'''
import logging
from django.shortcuts import render_to_response
from webui import settings, core
from django.template.context import RequestContext
from webui.abstracts import CoreService

logger = logging.getLogger(__name__)

def appdetails(request, appname):
    logger.debug("Application Details for %s" % appname)
    services = core.kermit_modules.extract(CoreService)
    service_status = []
    if services:
        for service in services:
            data = {"name": service.get_name(),
                    "description" : service.get_description(),
                    "status": service.get_status()}
            service_status.append(data)
    return render_to_response('platforms/application.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "appname": appname ,"service_status":service_status}, context_instance=RequestContext(request))
