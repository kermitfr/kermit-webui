'''
Created on Nov 5, 2011

@author: mmornati
'''
from webui.abstracts import CoreService
from webui.restserver import communication
from webui.core import kermit_modules
from webui.servicestatus.utils import check_service
from webui import settings

class RestService(CoreService):
    
    def get_name(self):
        return 'Rest'
    
    def get_description(self):
        return settings.RUBY_REST_PING_URL
    
    def get_status(self):
        return communication.verifyRestServer()
    
class CeleryService(CoreService):
    
    def get_name(self):
        return 'TaskMan'
    
    def get_description(self):
        return check_service('celeryd')
    
    def get_status(self):
        if (check_service('celeryd')):
            return True
        return False
    
class CeleryBeatService(CoreService):
    
    def get_name(self):
        return 'SchedMan'
    
    def get_description(self):
        return check_service('celerybeat')

    def get_status(self):
        if (check_service('celerybeat')):
            return True
        return False
    
class CeleryEvService(CoreService):
    
    def get_name(self):
        return 'SchedMon'
    
    def get_description(self):
        return check_service('celeryev')

    def get_status(self):
        if (check_service('celeryev')):
            return True
        return False
    
class KermitInventoryService(CoreService):
    
    def get_name(self):
        return 'InvQueue'
    
    def get_description(self):
        return check_service('kermit.inventory')

    def get_status(self):
        if (check_service('kermit.inventory')):
            return True
        return False
    
class KermitLogService(CoreService):
    
    def get_name(self):
        return 'LogQueue'
    
    def get_description(self):
        return check_service('kermit.log')

    def get_status(self):
        if (check_service('kermit.log')):
            return True
        return False
    
    
kermit_modules.register(RestService)
kermit_modules.register(CeleryService)
kermit_modules.register(CeleryBeatService)
kermit_modules.register(CeleryEvService)
kermit_modules.register(KermitInventoryService)
kermit_modules.register(KermitLogService)