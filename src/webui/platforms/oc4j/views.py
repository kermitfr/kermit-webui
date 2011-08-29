import logging
from webui import settings
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from communication import read_server_info
from webui.platforms.utils import convert_keys_names

logger = logging.getLogger(__name__)


def instanceInventory(request, hostname, instance_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        instance = None 
        for server in server_info:
            if server['id'] == instance_name:
                instance = server
                break 
        return render_to_response('platforms/oc4j/instance.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "java_stop_options":instance['java-stop-options'], "java_start_options":instance['java-start-options'], "oc4j_options":instance['oc4j-options'], "hostname": hostname}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/oc4j/instance.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))


def datasourceListInventory(request, hostname, instance_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        instance = None 
        for server in server_info:
            if server['id'] == instance_name:
                instance = server
                break 
        for datasource in instance['datasource']:
            convert_keys_names(datasource)
        return render_to_response('platforms/oc4j/datasources.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "datasources": instance['datasource']}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/oc4j/datasources.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))


def datasourceInventory(request, hostname, instance_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        instance = None 
        for server in server_info:
            if server['id'] == instance_name:
                instance = server
                break 
        resource_name = resource_name.replace('_', '/')
        datasource = None
        for current in instance['datasource']:
            if current['name'] == resource_name:
                datasource = current
                convert_keys_names(datasource)
                break
        return render_to_response('platforms/oc4j/datasource.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "datasource": datasource}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/oc4j/datasource.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))

def applicationInventory(request, hostname, instance_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        instance = None 
        for server in server_info:
            if server['id'] == instance_name:
                instance = server
                break
        selected_app = None 
        for app in instance['applilist']:
            if app['name'] == resource_name:
                selected_app = app
        #Retrieving datasource information
        for pool in selected_app['poollist']:
            for ds in instance['datasource']:
                if ds['name'] == pool['name']:
                    convert_keys_names(ds)  
                    pool['datasource'] = ds
                    break
        convert_keys_names(selected_app)        
        return render_to_response('platforms/oc4j/application.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL,"hostname":hostname, "instance_id":instance['id'] ,"application": selected_app}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/oc4j/application.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))


