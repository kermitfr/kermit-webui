'''
Created on Oct 25, 2011

@author: mmornati
'''
from webui.serverstatus.models import Server
from guardian.shortcuts import get_objects_for_user
import logging
from webui.platforms.weblogic.utils import extract_appli_info, check_contains,\
    extract_appli_details
from webui.platforms.abstracts import Application
from webui.platforms.platforms import platforms
from webui.platforms.weblogic import settings


logger = logging.getLogger(__name__)

class WebLogicApplication(Application):
    
    def getApplications(self, user):
        servers = Server.objects.filter(deleted=False)
        if user != 'fooUser':
            if not user.is_superuser:
                servers = get_objects_for_user(user, 'use_server', Server)
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
                    else:
                        applications.append(app)
    
        return applications
    
    def getAppliInfo(self, user, appname):
        servers = Server.objects.filter(deleted=False)
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
    
platforms.register(WebLogicApplication, settings.PLATFORM_NAME)