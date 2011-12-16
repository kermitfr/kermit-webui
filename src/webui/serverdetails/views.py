import logging
from django.shortcuts import render_to_response
from webui import settings, core
from django.template.context import RequestContext
from django.http import HttpResponse
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required
from webui.platforms.platforms import platforms
from webui.platforms.abstracts import ServerTree
from webui.abstracts import CoreService, ServerOperation
from django.core.urlresolvers import reverse
from webui.restserver.communication import callRestServer
from webui.serverstatus.models import Server

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
    services = core.kermit_modules.extract(CoreService)
    service_status = []
    if services:
        for service in services:
            data = {"name": service.get_name(),
                    "description" : service.get_description(),
                    "status": service.get_status()}
            service_status.append(data)
    my_server = Server.objects.get(hostname=hostname)
    operations = {}  
    server_operations = core.kermit_modules.extract(ServerOperation)
    if server_operations:
        for op in server_operations:
            if op.get_visible(my_server, request.user):
                group_name = 'nogroup'
                group_icon = None
                if op.get_group_name():
                    group_name = op.get_group_name()
                    group_icon = op.get_group_icon()
                data = {"img": op.get_image(),
                        "name": op.get_name(),
                        "url": op.get_url(hostname),
                        "hasparameters": op.request_parameters(),
                        "agent": op.get_agent(),
                        "action": op.get_action(),
                        "filter": op.get_filter(hostname),
                        "enabled": op.get_enabled(my_server),
                        "groupname": group_name,
                        "groupicon": group_icon}
                
                if not group_name in operations:
                    operations[group_name] = []
                operations[group_name].append(data)
            else:
                logger.debug("Operation %s is not visible for %s server" % (op.get_name(), hostname))

    #TODO: Make a refactor to remove base_url and statis_url from context
    return render_to_response('server/details.html', {"settings": settings, "base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "serverdetails": server_info, "hostname": hostname, "service_status":service_status, 'server_operations': operations}, context_instance=RequestContext(request))

@login_required()
def hostCallInventory(request, hostname):
    filters = "identity_filter=%s" % hostname
    response, content = callRestServer(request.user, filters, "rpcutil", "inventory", None, True)
    if response.status == 200:
        jsonObj = json.loads(content)
        return render_to_response('server/inventory.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname, 'service_status_url':settings.RUBY_REST_PING_URL, "c": jsonObj[0]}, context_instance=RequestContext(request))
    else:
        return render_to_response('server/inventory.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname, 'service_status_url':settings.RUBY_REST_PING_URL}, context_instance=RequestContext(request))
