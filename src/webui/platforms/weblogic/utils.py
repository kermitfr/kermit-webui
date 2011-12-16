'''
Created on Sep 22, 2011

@author: mmornati
'''
from webui.platforms.weblogic.communication import read_server_info
import logging
from webui.restserver.communication import callRestServer
from django.utils import simplejson as json

logger = logging.getLogger(__name__)

def extract_instances_name(hostname):
    instances = []
    server_info = read_server_info(hostname)
    if 'instances' in server_info:
        for instance in server_info['instances']:
            instances.append(instance['name'])
    return instances

def extract_appli_info(hostname, environment):
    applications = []
    server_info = read_server_info(hostname)
    if server_info: 
        for appli in server_info['applilist']:
            app = {"type":"Weblogic",
                   "name":appli["name"], 
                   "version":"",
                   "env":environment,
                   "servers":[{"server":hostname, "instance":appli['target']}],
                   "deploy":1}
            applications.append(app)
    return applications

def extract_appli_details(hostname, environment, appname):
    applications = []
    server_info = read_server_info(hostname)
    if server_info: 
        for appli in server_info['applilist']:
            if appli["name"] != appname:
                continue
            
            app = {"type":"Weblogic",
                       "name":appli["name"], 
                       "version":"",
                       "env":environment,
                       "server": hostname, 
                       "instance": appli['target']}
            applications.append(app)
    return applications


def check_contains(applications, appli):
    for app in applications:
        if app["type"] == appli["type"] and app["name"] == appli["name"] and app["version"] == appli["version"] and app["env"] == appli["env"]:
            return app
    return None

def get_apps_list(user, filters, file_type):
    logger.debug("Calling app_list with filters %s and type %s" % (filters, str(file_type)))
    try: 
        response, content = callRestServer(user, filters, "a7xows", "applist", "apptype="+str(file_type), False, False)
        if response.status == 200:
            jsonObj = json.loads(content)
            if jsonObj:
                #Looking for "intersections"
                app_list = None
                for server_response in jsonObj:
                    if server_response['statuscode']==0 and server_response['data']:
                        if not app_list:
                            app_list = server_response['data']['applist']
                        else:
                            app_list = list(set(app_list).intersection(server_response['data']['applist']))
                    else:
                        logger.warn("No app list received")
                return json.dumps({"errors":"", "applist":app_list})
            else:
                return json.dumps({"errors":"Cannot retrieve apps list"})
    except Exception, err:  
        logger.error('ERROR: ' + str(err))