'''
Created on Sep 22, 2011

@author: mmornati
'''
from webui.platforms.bar.communication import read_server_info
import logging
from webui.restserver.communication import callRestServer
from django.utils import simplejson as json

logger = logging.getLogger(__name__)


def extract_instances_name(hostname):
    consoles = []
    server_info = read_server_info(hostname)
    for console in server_info:
        consoles.append(console['consolename'])
        
    return consoles

def extract_appli_info(hostname, environment):
    applications = []
    server_info = read_server_info(hostname)
    if server_info: 
        for console in server_info:
            for bar in console['barlist']:
                version = ""
                if "version" in bar:
                    version = bar["version"]
                    
                app = {"type":"BAR",
                       "name":bar["name"],
                       "version":version,
                       "env":environment,
                       "servers":[{"server":hostname, "instance":console["consolename"]}],
                       "deploy":1}
                applications.append(app)
    return applications

def extract_appli_details(hostname, environment, barname):
    applications = []
    server_info = read_server_info(hostname)
    if server_info: 
        for console in server_info:
            for bar in console['barlist']:
                if bar["name"] != barname:
                    continue
                version = ""
                if "version" in bar:
                    version = bar["version"]
                    
                app = {"type":"OC4J",
                       "name":bar["name"],
                       "version":version,
                       "env":environment,
                       "server": hostname,
                       "resources":bar["resources"],
                       "instance": console["consolename"]}
                applications.append(app)
    return applications

def check_contains(applications, appli):
    for app in applications:
        if app["type"] == appli["type"] and app["name"] == appli["name"] and app["version"] == appli["version"] and app["env"] == appli["env"]:
            return app
    return None

def get_available_bars(user, filters):
    logger.debug("Calling bar_list with filters %s" % (filters))
    try: 
        response, content = callRestServer(user, filters, "a7xbar", "applist", "apptype=%s" % 'bar', False, False)
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
                        logger.warn("No bar list response received")
                return json.dumps({"errors":"", "applist":app_list})
            else:
                return json.dumps({"errors":"Cannot retrieve apps list"})
    except Exception, err:  
        logger.error('ERROR: ' + str(err))
