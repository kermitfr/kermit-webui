'''
Created on Aug 12, 2011

@author: mmornati
'''
from kermit.widgets.base import Widget
from kermit.defaultop.models import Operation

class DashBoardDefaultOps(Widget):
    template = "widgets/basecommands.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        operations = Operation.objects.filter(enabled=True)
        widget_context = {"operations":operations}
        return dict(super_context.items() + widget_context.items())
    
class DashBoardOpResults(Widget):
    template = "widgets/opresponse.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        return super_context
    
    
    
