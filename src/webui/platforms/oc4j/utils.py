'''
Created on Sep 22, 2011

@author: mmornati
'''
from webui.platforms.oc4j.communication import read_server_info
from webui.restserver.communication import callRestServer
import logging
from django.utils import simplejson as json

logger = logging.getLogger(__name__)

def extract_instances_name(hostname):
    instances = []
    server_info = read_server_info(hostname)
    for instance in server_info:
        instances.append(instance['id'])
        
    return instances

def get_apps_list(user, filters, file_type):
    logger.debug("Calling app_list with filters %s and type %s" % (filters, str(file_type)))
    try: 
        response, content = callRestServer(user, filters, "a7xoas", "applist", "apptype="+str(file_type))
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
                return json.dumps({"errors":"", "applist":app_list})
            else:
                return json.dumps({"errors":"Cannot retrieve apps list"})
    except Exception, err:  
        logger.error('ERROR: ' + str(err))

def extract_appli_info(hostname, environment):
    applications = []
    server_info = read_server_info(hostname)
    if server_info: 
        for instance in server_info:
            for appli in instance['applilist']:
                version = ""
                if "appliver" in appli and "version" in appli["appliver"]:
                    version = appli["appliver"]["version"]
                    
                app = {"type":"OC4J",
                       "name":appli["name"], 
                       "version":version,
                       "env":environment,
                       "servers":[{"server":hostname, "instance":instance["id"]}],
                       "deploy":1}
                applications.append(app)
    return applications

def extract_appli_details(hostname, environment, appname):
    applications = []
    server_info = read_server_info(hostname)
    if server_info: 
        for instance in server_info:
            for appli in instance['applilist']:
                if appli["name"] != appname:
                    continue
                version = ""
                if "appliver" in appli and "version" in appli["appliver"]:
                    version = appli["appliver"]["version"]
                    
                app = {"type":"OC4J",
                       "name":appli["name"], 
                       "version":version,
                       "env":environment,
                       "server": hostname, 
                       "instance": instance["id"]}
                applications.append(app)
    return applications

def check_contains(applications, appli):
    for app in applications:
        if app["type"] == appli["type"] and app["name"] == appli["name"] and app["version"] == appli["version"] and app["env"] == appli["env"]:
            return app
    return None