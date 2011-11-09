'''
Created on Oct 25, 2011

@author: mmornati
'''
from webui.serverstatus.models import Server
from guardian.shortcuts import get_objects_for_user
import logging
from webui.platforms.jboss.utils import extract_appli_info, check_contains,\
    extract_appli_details
from webui.platforms.abstracts import Application
from webui.platforms.jboss import settings
from webui.platforms.platforms import platforms
from webui.serverdetails import utils


logger = logging.getLogger(__name__)

class JBossApplication(Application):

    def getApplications(self, user):
        servers = utils.extract_user_servers(user)
        #Retrieving applilist for any server controlled by kermit
        applications = []
        for server in servers:
            environment = self.extract_environment_level(server)  
            appli = extract_appli_info(server.hostname, environment)
            if appli:
                for app in appli:
                    extracted = check_contains(applications, app)
                    if extracted:
                        extracted["deploy"] = extracted["deploy"] + 1
                        extracted["servers"].append(app["servers"])
                    else:
                        applications.append(app)
        return applications
    
    def getApplicationsPath(self, user, server_path):
        servers = utils.extract_user_servers_in_path(user, server_path)
        #Retrieving applilist for any server controlled by kermit
        applications = []
        for server in servers:
            environment = self.extract_environment_level(server)  
            appli = extract_appli_info(server.hostname, environment)
            if appli:
                for app in appli:
                    extracted = check_contains(applications, app)
                    if extracted:
                        extracted["deploy"] = extracted["deploy"] + 1
                        extracted["servers"].append(app["servers"])
                    else:
                        applications.append(app)
        return applications
    
    def getAppliInfo(self, user, appname):
        servers = utils.extract_user_servers(user)
        if user != 'fooUser':
            if not user.is_superuser:
                servers = get_objects_for_user(user, 'use_server', Server)
        #Retrieving applilist for any server controlled by kermit
        applications = []
        for server in servers:
            environment = self.extract_environment_level(server)  
            appli = extract_appli_details(server.hostname, environment, appname)
            if appli:
                applications.extend(appli)
        return applications
    
platforms.register(JBossApplication, settings.PLATFORM_NAME)