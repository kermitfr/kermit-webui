'''
Created on Aug 12, 2011

@author: mmornati
'''
from webui.widgets.base import Widget
from webui.puppetclasses.models import PuppetClass

class DashBoardPuppetClasses(Widget):
    template = "widgets/puppetclasses.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        classes = PuppetClass.objects.filter(enabled=True, parent=None)
        widget_context = {"classes":classes}
        return dict(super_context.items() + widget_context.items())
    
    
    
