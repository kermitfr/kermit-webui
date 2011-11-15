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
    
    def get_status(self):
        raise NotImplementedAbstract
    
class ServerOperation(object):
    
    def execute(self):
        raise NotImplementedAbstract