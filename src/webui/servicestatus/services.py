'''
Created on Nov 5, 2011

@author: mmornati
'''
from webui.abstracts import CoreService
from webui.restserver import communication
from webui.core import kermit_modules

class RestService(CoreService):
    
    def get_status(self):
        services = {}
        services['restserver'] = communication.verifyRestServer()
        return services
    
    
kermit_modules.register(RestService)