import logging
from webui import settings
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from communication import read_server_info
from webui.platforms.utils import convert_keys_names

logger = logging.getLogger(__name__)


def instanceInventory(request, hostname, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        selected_instance = None
        for instance in server_info["instances"]:
            if instance['name'] == resource_name:
                selected_instance = instance
                break
        convert_keys_names(selected_instance)
        return render_to_response('platforms/weblogic/instance.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL,"hostname":hostname, "instance": selected_instance}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/weblogic/instance.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))


def datasourceInventory(request, hostname, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        selected_datasource = None
        for datasource in server_info["datasources"]:
            if datasource['name'] == resource_name:
                selected_datasource = datasource
                break
        convert_keys_names(selected_datasource)
        return render_to_response('platforms/weblogic/datasource.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL,"hostname":hostname, "datasource": datasource}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/weblogic/datasource.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))


def consoleInventory(request, hostname, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        db_console = server_info["console"]
        convert_keys_names(db_console)
        return render_to_response('platforms/weblogic/console.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL,"hostname":hostname, "console": db_console}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/weblogic/console.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))

def nodeManagerInventory(request, hostname, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        #TODO: Modify and add managing of more than one nodemanager
        db_nodemanager = server_info["nodemanagers"][0]
        convert_keys_names(db_nodemanager)
        return render_to_response('platforms/weblogic/nodemanager.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL,"hostname":hostname, "nodemanager": db_nodemanager}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/weblogic/nodemanager.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))

def applicationInventory(request, hostname, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        selected_app = None
        for app in server_info["applilist"]:
            if app['name'] == resource_name:
                selected_app = app
                break
        convert_keys_names(selected_app)
        return render_to_response('platforms/weblogic/application.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL,"hostname":hostname, "application": selected_app}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/weblogic/application.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))
