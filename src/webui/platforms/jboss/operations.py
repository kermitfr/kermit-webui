'''
Created on Nov 8, 2011

@author: mmornati
'''
from webui.abstracts import ContextOperation
from webui import settings
from webui.core import kermit_modules

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
    
kermit_modules.register(JbossDeployContextMenu)
kermit_modules.register(JbossLogContextMenu)