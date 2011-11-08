'''
Created on Sep 22, 2011

@author: mmornati
'''
from webui.platforms.bar.communication import read_server_info


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