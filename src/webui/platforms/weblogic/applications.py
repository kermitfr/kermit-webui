'''
Created on Oct 25, 2011

@author: mmornati
'''
from webui.serverstatus.models import Server
from guardian.shortcuts import get_objects_for_user
import logging
from webui.platforms.weblogic.utils import extract_appli_info
from webui.utils import CONF


logger = logging.getLogger(__name__)

def getApplications(user):
    servers = Server.objects.filter(deleted=False)
    if user != 'fooUser':
        if not user.is_superuser:
            servers = get_objects_for_user(user, 'use_server', Server)
    #Retrieving applilist for any server controlled by kermit
    applications = []
    level = CONF.getint("webui", "environment.level")
    for server in servers:
        environment = ""
        #You can change the environment level in your puppet classes hierarchy 
        #In kermit configuration file
        for puppetclass in server.puppet_classes.values():
            if puppetclass["level"]==level:
                environment = puppetclass["name"]
                break
        appli = extract_appli_info(server.hostname, environment)
        if appli:
            applications.extend(appli)

    return applications