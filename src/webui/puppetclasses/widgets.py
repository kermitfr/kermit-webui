'''
Created on Aug 12, 2011

@author: mmornati
'''
from webui.widgets.base import Widget
from webui.puppetclasses.models import PuppetClass
from webui.agent.models import Agent
from webui.defaultop.models import Operation

class DashBoardPuppetClasses(Widget):
    template = "widgets/puppetclasses/puppetclasses.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        agents = Agent.objects.filter(enabled=True)
        operations = Operation.objects.filter(enabled=True)
        widget_context = {"agents":agents, "operations":operations}
        return dict(super_context.items() + widget_context.items())
    
    
    
