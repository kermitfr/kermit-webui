'''
Created on Aug 12, 2011

@author: mmornati
'''
from webui.widgets.base import Widget
from webui.puppetclasses.models import PuppetClass
from webui.agent.models import Agent, Action
from webui.defaultop.models import Operation
from guardian.shortcuts import get_objects_for_user

class DashBoardPuppetClasses(Widget):
    template = "widgets/puppetclasses/puppetclasses.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        agents = Agent.objects.filter(enabled=True)
        actions = {}
        if not self.user.is_superuser:
            agents = get_objects_for_user(self.user, 'use_agent', Agent).filter(enabled=True)
            #Fix added to filter agents actions on set acls
            for agent in agents:
                if not self.user.is_superuser:
                    current_actions = get_objects_for_user(self.user, 'use_action', Action).filter(agent=agent)
                    actions[agent.name] = current_actions
        operations = Operation.objects.filter(enabled=True)
        if not self.user.is_superuser:
            operations = get_objects_for_user(self.user, 'execute_operation', Operation).filter(enabled=True)
        widget_context = {"agents":agents, "operations":operations, "actions": actions}
        return dict(super_context.items() + widget_context.items())
    
    
    
