'''
Created on Nov 5, 2011

@author: mmornati
'''
from webui.exceptions import NotImplementedAbstract


class ContextOperation(object):

    type = 'undefined'
    
    def get_operations(self):
        raise NotImplementedAbstract
        
        
class CoreService(object):
    
    def get_name(self):
        raise NotImplementedAbstract
    
    def get_description(self):
        raise NotImplementedAbstract
    
    def get_status(self):
        raise NotImplementedAbstract
    
class ServerOperation(object):
    
    def get_visible(self, server):
        raise NotImplementedAbstract
    
    def get_enabled(self, server):
        raise NotImplementedAbstract
    
    def get_name(self):
        raise NotImplementedAbstract
    
    def get_image(self):
        raise NotImplementedAbstract
    
    def get_group_name(self):
        return None
    
    def get_group_icon(self):
        return None
    
    def request_parameters(self):
        return False
    
    def get_agent(self):
        return ''
    
    def get_action(self):
        return ''
    
    def get_filter(self, hostname):
        return ''
    
    def get_url(self, hostname, instancename):
        raise NotImplementedAbstract