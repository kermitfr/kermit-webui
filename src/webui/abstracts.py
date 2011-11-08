'''
Created on Nov 5, 2011

@author: mmornati
'''
from webui.exceptions import NotImplementedAbstract


class ContextOperation(object):
    
    def execute_operation(self):
        raise NotImplementedAbstract
        
        
class CoreService(object):
    
    def get_status(self):
        raise NotImplementedAbstract