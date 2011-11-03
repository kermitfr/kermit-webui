# Create your views here.
from webui.platforms.bar.communication import read_server_info
from django.contrib.auth.decorators import login_required
from webui.platforms.utils import convert_keys_names
from django.shortcuts import render_to_response
from webui import settings
from django.template.context import RequestContext
import logging

logger = logging.getLogger(__name__)

@login_required()
def poolInventory(request, hostname, console_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        selected_console = None 
        for console in server_info:
            if console['consolename'] == console_name:
                selected_console = console
                break 
        resource_name = resource_name.replace('_', '/')
        pool = None
        for current in selected_console['poollist']:
            if current['poolname'] == resource_name:
                pool = current
                convert_keys_names(pool)
                break
        return render_to_response('platforms/bar/datasource.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "datasource": pool}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/bar/datasource.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))

@login_required()
def poolsInventory(request, hostname, console_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        selected_console = None 
        for console in server_info:
            if console['consolename'] == console_name:
                selected_console = console
                break 
        resource_name = resource_name.replace('_', '/')
        return render_to_response('platforms/bar/datasources.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "datasources": selected_console['poollist']}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/bar/datasources.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))


@login_required()
def barInventory(request, hostname, console_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        selected_console = None 
        for console in server_info:
            if console['consolename'] == console_name:
                selected_console = console
                break 
        selected_bar = None 
        for bar in selected_console['barlist']:
            if bar['name'] == resource_name:
                selected_bar = bar
                break
        #Retrieving datasource information
        if "resources" in selected_bar:
            pool_info = []
            for pool in selected_bar['resources']:
                for retrieved_ds in selected_console['poollist']:
                    if retrieved_ds['poolname'] == pool:
                        convert_keys_names(retrieved_ds)  
                        pool_info.append(retrieved_ds)
                        break
            selected_bar['datasources'] = pool_info    
        else:
            logger.debug("No poollist key found for %s" % console['consolename'])
            
        convert_keys_names(selected_bar)        
        return render_to_response('platforms/bar/batch.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL,"hostname":hostname, "bar":selected_bar}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/bar/batch.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))


@login_required()
def barConsoleInventory(request, hostname, console_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        selected_console = None 
        for console in server_info:
            if console['consolename'] == console_name:
                selected_console = console
                break 
        
        if 'java_ver' in selected_console:
            java_version = selected_console["java_ver"]
        else:
            java_version = ""
              
        return render_to_response('platforms/bar/console.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL,"hostname":hostname, "java_version":java_version}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/bar/console.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))
