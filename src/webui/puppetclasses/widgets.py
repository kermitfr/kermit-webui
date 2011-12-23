'''
Created on Aug 12, 2011

@author: mmornati
'''
from webui.widgets.base import Widget
from webui.agent.models import Agent, Action
from webui.defaultop.models import Operation
from guardian.shortcuts import get_objects_for_user
from webui.core import kermit_modules
from webui.abstracts import ContextOperation
import logging

logger = logging.getLogger(__name__)

class DashBoardPuppetClasses(Widget):
    template = "widgets/puppetclasses/puppetclasses.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        agents = Agent.objects.filter(enabled=True)
        actions = {}
        if not self.user.is_superuser:
            if self.user.has_perm('agent.show_widget_agent'):
                agents = get_objects_for_user(self.user, 'use_agent', Agent).filter(enabled=True)
                #Fix added to filter agents actions on set acls
                for agent in agents:
                    if not self.user.is_superuser:
                        current_actions = get_objects_for_user(self.user, 'use_action', Action).filter(agent=agent)
                        actions[agent.name] = current_actions
                if not actions:
                    agents = {}
            else: 
                agents = {}
        operations = Operation.objects.filter(enabled=True)
        if not self.user.is_superuser:
            operations = get_objects_for_user(self.user, 'execute_operation', Operation).filter(enabled=True)
            
        context_operations = kermit_modules.extract(ContextOperation)
        automatic_operations = {}
        if context_operations:
            for c_op in context_operations:
                if c_op.get_enabled(self.user):
                    menu_name = "Undefined"
                    if c_op.get_type():
                        menu_name = c_op.get_type()
                    if not menu_name in automatic_operations:
                        automatic_operations[menu_name] = []
                    automatic_operations[menu_name].extend(c_op.get_operations())
                else:
                    logger.debug("Excluding operation %s. Not enabled for user %s" % (c_op.get_type(), self.user))
        widget_context = {"agents":agents, "operations":operations, "actions": actions, 'automatic_operations':automatic_operations}
        return dict(super_context.items() + widget_context.items())
    
    
    
