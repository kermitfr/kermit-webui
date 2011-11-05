'''
Created on Nov 5, 2011

@author: mmornati
'''
from reportlab.graphics.shapes import NotImplementedError


class ContextOperation(object):
    
    
    
    def execute_operation(self):
        raise NotImplementedError
        
        
class CoreService(object):
    
    def get_status(self):
        raise NotImplementedError