'''
Created on Sep 22, 2011

@author: mmornati
'''
from webui.platforms.oc4j.communication import read_server_info


def extract_instances_name(hostname):
    instances = []
    server_info = read_server_info(hostname)
    for instance in server_info:
        instances.append(instance['id'])
        
    return instances

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