'''
Created on Nov 4, 2011

@author: mmornati
'''
from webui.utils import CONF
import ConfigParser
import logging

logger = logging.getLogger(__name__)

class ServerTree(object):
    '''
    Abstract Class to define elements that inject stuffs in 
    the server details tree
    '''
    def getDetails(self, hostname):
        raise NotImplementedError
    
    
    
class UpdatePlatform(object):
    '''
    Abstract Class to define platforms with one (or more)
    updates method
    '''
    def inventoryUpdate(self, user):
        raise NotImplementedError
    

class Application(object):
    '''
    Abstract Class to define platform containing applications information
    Like, for example, the ApplicationServer has the application concept
    '''
    def getApplications(self, user):
        raise NotImplementedError
    
    def getAppliInfo(self, user, appname):
        raise NotImplementedError
    
    def extract_environment_level(self, server):
        try:
            level = CONF.getint("webui", "environment.level")
        except ConfigParser.NoOptionError:
            logger.error("Cannot find environment.level variable. Environment information won't be shown in webui")
            return ""
        #You can change the environment level in your puppet classes hierarchy 
        #In kermit configuration file
        for puppetclass in server.puppet_classes.values():
            if puppetclass["level"]==level:
                environment = puppetclass["name"]
                return environment
