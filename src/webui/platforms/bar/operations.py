'''
Created on Nov 8, 2011

@author: mmornati
'''
from webui.abstracts import ContextOperation
from webui import settings
from webui.core import kermit_modules
from guardian.shortcuts import get_objects_for_user
from webui.agent.models import Agent, Action

class BarDeployContextMenu(ContextOperation):
    
    def get_operations(self):
        context_menu_ops = []
        context_menu_ops.append(
            {"name":"deploy_bar",
             "description":"Deploy BAR",
             "javascript":"getDeployForm('%s', 'bar', 'deploy-dialog', 'deploy', '$$filterlist$$')" % settings.BASE_URL,
             "server_operation":"",
             })
        return context_menu_ops
    
    def get_type(self):
        return 'BAR'
    
    def get_visible(self, server):
        agent = server.agents.filter(name='a7xbar')
        return len(agent)==1
    
    def get_enabled(self, user):
        if not user.is_superuser:
            agents = get_objects_for_user(user, 'use_agent', Agent).filter(enabled=True, name="a7xbar")
            if len(agents)==1:
                action = get_objects_for_user(user, 'use_action', Action).filter(agent=agents[0], name="deploy")
                return action and len(action)==1
            else:
                return False
        else:
            return True
    

kermit_modules.register(BarDeployContextMenu)
