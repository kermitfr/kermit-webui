import logging
from django.shortcuts import render_to_response
from webui import settings, core
from django.template.context import RequestContext
from django.http import HttpResponse
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required
from webui.platforms.platforms import platforms
from webui.platforms.abstracts import ServerTree
from webui.abstracts import ServerOperation
from django.core.urlresolvers import reverse
from webui.restserver.communication import callRestServer
from webui.servers.models import Server
from webui.core import generate_commons_page_dict
from webui.servers.utils import get_server_operations

logger = logging.getLogger(__name__)

@login_required()
def getDetailsTree(request, hostname):
    #Entering in any platform an collect tree info
    logger.debug('Collecting platform trees')
    data = []
    content = {"isFolder": True, "expand": True, "title": hostname, "key":hostname, "icon":"server.png", "detailsEnabled":"true", 'url': reverse('server_inventory_details', kwargs={'hostname':hostname})}
    children = []
    tree_modules = platforms.extract(ServerTree)
    if tree_modules:
        for current in tree_modules:
            platform_data = current.getDetailsTree(hostname)
            if platform_data:
                children.append(platform_data)
        
    content['children'] = children
    data.append(content)
    return HttpResponse(json.dumps(data))

@login_required()
def hostInventory(request, hostname):
    server_info = []   
    return render_to_response('server/details.html', dict({"serverdetails": server_info, "hostname": hostname, 'server_operations': get_server_operations(request,hostname)}, **generate_commons_page_dict(request)), context_instance=RequestContext(request))

@login_required()
def hostCallInventory(request, hostname):
    filters = "identity=%s" % hostname
    response, content = callRestServer(request.user, filters, "rpcutil", "inventory", None, True)
    if response.getStatus() == 200:
        jsonObj = []
        for entry in content:
            jsonObj.append(entry.to_dict())
            
        return render_to_response('server/inventory.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname, 'service_status_url':settings.RUBY_REST_PING_URL, "c": jsonObj[0]}, context_instance=RequestContext(request))
    else:
        return render_to_response('server/inventory.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname, 'service_status_url':settings.RUBY_REST_PING_URL}, context_instance=RequestContext(request))