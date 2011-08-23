
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
    return render_to_response('server/details.html', {"base_url": settings.BASE_URL, "serverdetails": server_info, "hostname": hostname}, context_instance=RequestContext(request))

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
            db = {'title':instance['id'], "key":instance['id'], "icon":"web_instance.png", "type":"instance"}
            #Configuring Applications
            logger.debug('Configuring Applications')
            applications = {'title': 'Applications', 'isFolder':"true", "key":"applications", "icon":"folder_applications.png", "type":"applications"}
            apps = []
            for appli in instance['applilist']:
                app = {'title':appli['name'], "key":appli['name'], "type":"application"}
                apps.append(app)
            applications['children'] = apps
            
            #Configuring Datasources
            logger.debug('Configuring Datasources')
            datasources = {'title': 'Datasources', 'isFolder':"true", "key":"datasources", "icon":"folder_database.png", "type":"datasources"}
            dss = []
            for datasource in instance['datasource']:
                datasource = {'title':datasource['name'], "key":datasource['name'], "type":"datasource"}
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

def instanceInventory(request, hostname, instance_name):
    server_info = read_server_info(hostname)
    if server_info:
        instance = None 
        for server in server_info:
            if server['id'] == instance_name:
                instance = server
                break 
        for datasource in instance['datasource']:
            convert_keys_names(datasource)
        return render_to_response('server/instance.html', {"base_url": settings.BASE_URL, "datasources": instance['datasource'], "java_stop_options":instance['java-stop-options'], "java_start_options":instance['java-start-options'], "oc4j_options":instance['oc4j-options'], "hostname": hostname}, context_instance=RequestContext(request))
    else:
        return render_to_response('server/instance.html', {"base_url": settings.BASE_URL, "hostname": hostname}, context_instance=RequestContext(request))
