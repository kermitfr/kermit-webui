'''
Created on Sep 22, 2011

@author: mmornati
'''
from webui.platforms.weblogic.communication import read_server_info


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