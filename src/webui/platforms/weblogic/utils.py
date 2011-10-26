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
                   "deploy":""}
            applications.append(app)
    return applications