'''
Created on Aug 12, 2011

@author: mmornati
'''
from webui.widgets.base import Widget
from webui.defaultop.models import Operation
from guardian.shortcuts import get_objects_for_user
from webui import settings

class DashBoardDefaultOps(Widget):
    template = "widgets/defaultop/basecommands.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        operations = Operation.objects.filter(enabled=True)
        if not self.user.is_superuser:
            operations = get_objects_for_user(self.user, 'execute_operation', Operation).filter(enabled=True)
        widget_context = {"operations":operations, "base_url":settings.BASE_URL}
        return dict(super_context.items() + widget_context.items())
    
class DashBoardOpResults(Widget):
    template = "widgets/defaultop/opresponse.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        return super_context
    
    
    
