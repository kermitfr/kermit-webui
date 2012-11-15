'''
Created on Nov 3, 2011

@author: mmornati
'''
import logging
from webui.abstracts import CoreService
from webui import settings as kermitsettings
from webui.utils import read_kermit_version

logger = logging.getLogger(__name__)

def generate_commons_page_dict(request):
    services = kermit_modules.extract(CoreService)
    service_status = []
    show_status_bar = request.user.is_superuser or kermitsettings.SHOW_STATUS_BAR 
    if services and show_status_bar:
        for service in services:
            data = {"name": service.get_name(),
                    "description" : service.get_description(),
                    "status": service.get_status()}
            service_status.append(data)
    version = read_kermit_version()
    
    return {"settings": kermitsettings, 
            "base_url": kermitsettings.BASE_URL, 
            "static_url":kermitsettings.STATIC_URL,
            'service_status_url':kermitsettings.RUBY_REST_PING_URL,
            "service_status":service_status, 
            "kermit_version":version} 


class KermitMcoResponse(object):
    
    def __init__(self, status=None):
        self.status = status
        
    def getStatus(self):
        return self.status
        
class KermitMcoContent(object):
    
    def __init__(self, data=None, status_code=None, sender=None, status_message=None):
        self.data = data
        self.status_code = status_code
        self.sender = sender
        self.status_message = status_message
        
    def getData(self):
        return self.data
    
    def getStatusCode(self):
        return self.status_code
    
    def getSender(self):
        return self.sender
    
    def getStatusMessage(self):
        return self.status_message
    
    def to_dict(self):
        return {"data":self.data, "statuscode":self.status_code,"sender":self.sender,"statusmsg":self.status_message}
        
    
        

class KermitModule(object):

    def __init__(self, name=None, platform_name=None):
        self._registry = {} 
        self.root_path = None
        self.name = name

    def register(self, core_class):
        group_class = core_class.__base__
        if group_class in self._registry: 
            self._registry[group_class].append(core_class())
        else:
            self._registry[group_class] = [core_class()]

    
    def extract(self, base_class):
        if base_class in self._registry:
            return self._registry[base_class]
        else:
            logger.warn("No class registered with %s BaseClass" % base_class)
        
        return None
                
        

kermit_modules = KermitModule()