'''
Created on Nov 8, 2011

@author: mmornati
'''
from webui.abstracts import ContextOperation
from webui import settings
from webui.core import kermit_modules
from guardian.shortcuts import get_objects_for_user
from webui.agent.models import Agent, Action

class JbossDeployContextMenu(ContextOperation):
    
    def get_operations(self):
        context_menu_ops = []
        context_menu_ops.append(
            {"name":"deploy_jboss",
             "description":"Deploy Application",
             "javascript":"getDeployForm('%s', 'jboss', 'deploy-dialog', 'deploy', '$$filterlist$$')" % settings.BASE_URL,
             "server_operation":"",
             })
        return context_menu_ops
    
    def get_type(self):
        return 'JBoss'
    
    def get_visible(self, server):
        agent = server.agents.filter(name='jboss')
        return len(agent)==1
    
    def get_enabled(self, user):
        if not user.is_superuser:
            agents = get_objects_for_user(user, 'use_agent', Agent).filter(enabled=True, name="jboss")
            if len(agents)==1:
                action = get_objects_for_user(user, 'use_action', Action).filter(agent=agents[0], name="deploy")
                return action and len(action)==1
            else:
                return False
        else:
            return True
    
class JbossLogContextMenu(ContextOperation):
    
    def get_operations(self):
        context_menu_ops = []
        context_menu_ops.append(
            {"name":"get_log_jboss",
             "description":"Get Server Log",
             "javascript":"getLogForm('%s', 'jboss', 'deploy-dialog', 'get_log', '$$filterlist$$')" % settings.BASE_URL,
             "server_operation":"",
             })
        return context_menu_ops
    
    def get_type(self):
        return 'JBoss'
    
    def get_visible(self, server):
        agent = server.agents.filter(name='jboss')
        return len(agent)==1
    
    def get_enabled(self, user):
        if not user.is_superuser:
            agents = get_objects_for_user(user, 'use_agent', Agent).filter(enabled=True, name="jboss")
            if len(agents)==1:
                action = get_objects_for_user(user, 'use_action', Action).filter(agent=agents[0], name="get_log")
                return action and len(action)==1
            else:
                return False
        else:
            return True
    
kermit_modules.register(JbossDeployContextMenu)
kermit_modules.register(JbossLogContextMenu)