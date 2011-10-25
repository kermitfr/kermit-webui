import logging
from django.shortcuts import render_to_response
from webui import settings
from webui.platforms import settings as platform_settings
from django.template.context import RequestContext
import imp
from django.http import HttpResponse
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required
from webui.servicestatus import utils

logger = logging.getLogger(__name__)

@login_required()
def getDetailsTree(request, hostname):
    #Entering in any platform an collect tree info
    logger.debug('Collecting platform trees')
    data = []
    content = {"isFolder": "true", "expand": True, "title": hostname, "key":hostname, "icon":"server.png"}
    children = []
    for platform in platform_settings.INSTALLED_PLATFORMS:
        #TODO: Make this part dynamic
        platform_name = 'webui.platforms.' + platform
        try:
            platform_path = __import__(platform_name, {}, {}, [platform_name.split('.')[-1]]).__path__
        except AttributeError:
            continue
        
        try:
            fp, pathname, description = imp.find_module('tree', platform_path)
            mod = imp.load_module('tree', fp, pathname, description)
            platform_data = mod.getDetailsTree(hostname)
            if platform_data:
                children.append(platform_data)
        except:
            logger.debug('No module tree found for %s' % platform_path)
    
    content['children'] = children
    data.append(content)
    return HttpResponse(json.dumps(data))

@login_required()
def hostInventory(request, hostname):
    server_info = []   
    service_status = None
    if 'webui.servicestatus' in settings.INSTALLED_APPS:
        service_status = utils.test_services() 
    return render_to_response('server/details.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "serverdetails": server_info, "hostname": hostname, "service_status":service_status, 'service_status_url':settings.RUBY_REST_PING_URL}, context_instance=RequestContext(request))
