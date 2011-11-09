'''
Created on Sep 22, 2011

@author: mmornati
'''
from webui.platforms.jboss.communication import read_server_info
from webui.restserver.communication import callRestServer
import logging
from django.utils import simplejson as json

logger = logging.getLogger(__name__)

def extract_instances_name(hostname):
    instances = []
    server_info = read_server_info(hostname)
    for instance in server_info["instances"]:
        instances.append(instance['name'])
        
    return instances

def get_apps_list(user, filters, file_type):
    logger.debug("Calling app_list with filters %s and type %s" % (filters, str(file_type)))
    try: 
        response, content = callRestServer(user, filters, "jboss", "applist", "apptype="+str(file_type))
        if response.status == 200:
            jsonObj = json.loads(content)
            if jsonObj:
                #Looking for "intersections"
                app_list = None
                for server_response in jsonObj:
                    if not app_list:
                        app_list = server_response['data']['applist']
                    else:
                        app_list = set(app_list).intersection(server_response['data']['applist'])
                
                #If I test the intersection I need to re-convert my object to list
                if type(app_list) == set:
                    app_list = list(app_list)
                return json.dumps({"errors":"", "applist":app_list})
            else:
                return json.dumps({"errors":"Cannot retrieve apps list"})
    except Exception, err:  
        logger.error('ERROR: ' + str(err))