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