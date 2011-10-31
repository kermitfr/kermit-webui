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
                       "deploy":""}
                applications.append(app)
    return applications