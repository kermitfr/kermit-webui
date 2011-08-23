
import logging
from webui import settings
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from webui.serverdetails.utils import read_server_info, convert_keys_names
from django.utils import simplejson as json
from django.http import HttpResponse

logger = logging.getLogger(__name__)


def hostInventory(request, hostname):
    server_info = read_server_info(hostname)    
    if not server_info:
        server_info = []
    return render_to_response('server/details.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "serverdetails": server_info, "hostname": hostname}, context_instance=RequestContext(request))

def getDetailsTree(request, hostname):
    data = []
    content = {"isFolder": "true", "title": hostname, "key":hostname, "icon":"server.png"}
    server_info = read_server_info(hostname)
    #Configuring Instances
    if server_info:
        logger.debug('Configuring Instances')
        db_instances = {'title': 'Instances', 'isFolder':"true", "key":"instance", "icon":"app_server.png", "type":"instances"}
        dbs = []
        for instance in server_info:
            db = {'title':instance['id'], "key":instance['id'], "icon":"web_instance.png", "type":"instance", "instance":instance['id'],"detailsEnabled":"true"}
            #Configuring Applications
            logger.debug('Configuring Applications')
            applications = {'title': 'Applications', 'isFolder':"true", "key":"applications", "icon":"folder_applications.png", "type":"applications"}
            apps = []
            for appli in instance['applilist']:
                app = {'title':appli['name'], "key":appli['name'], "icon":"application.png", "type":"application", "instance":instance['id'], "detailsEnabled":"true"}
                apps.append(app)
            applications['children'] = apps
            
            #Configuring Datasources
            logger.debug('Configuring Datasources')
            datasources = {'title': 'Datasources', 'isFolder':"true", "key":"datasources", "icon":"folder_database.png", "type":"datasources", "instance":instance['id'], "detailsEnabled":"true"}
            dss = []
            for datasource in instance['datasource']:
                datasource = {'title':datasource['name'], "key":datasource['name'], "icon":"datasource.png", "type":"datasource", "instance":instance['id']}
                dss.append(datasource)
            datasources['children'] = dss
            
            db['children'] = [datasources, applications]
            dbs.append(db)
        db_instances['children'] = dbs
        
        children = []
        children.append(db_instances)
        content['children'] = children 
    data.append(content)
    return HttpResponse(json.dumps(data))

def instanceInventory(request, hostname, instance_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        instance = None 
        for server in server_info:
            if server['id'] == instance_name:
                instance = server
                break 
        return render_to_response('server/instance.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "java_stop_options":instance['java-stop-options'], "java_start_options":instance['java-start-options'], "oc4j_options":instance['oc4j-options'], "hostname": hostname}, context_instance=RequestContext(request))
    else:
        return render_to_response('server/instance.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))


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
        return render_to_response('server/datasource.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "datasources": instance['datasource']}, context_instance=RequestContext(request))
    else:
        return render_to_response('server/datasource.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))


def datasourceInventory(request, hostname, instance_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        instance = None 
        for server in server_info:
            if server['id'] == instance_name:
                instance = server
                break 
        for datasource in instance['datasource']:
            convert_keys_names(datasource)
        return render_to_response('server/datasource.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "datasources": instance['datasource']}, context_instance=RequestContext(request))
    else:
        return render_to_response('server/datasource.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))

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
                convert_keys_names(selected_app)
        return render_to_response('server/application.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL,"hostname":hostname, "instance_id":instance['id'] ,"application": selected_app}, context_instance=RequestContext(request))
    else:
        return render_to_response('server/application.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))

