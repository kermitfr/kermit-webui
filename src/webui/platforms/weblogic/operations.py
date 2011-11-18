'''
Created on Nov 8, 2011

@author: mmornati
'''
from webui.abstracts import ContextOperation, ServerOperation
from webui import settings
from webui.core import kermit_modules

class WeblogicDeployContextMenu(ContextOperation):
    
    def get_operations(self):
        context_menu_ops = []
        context_menu_ops.append(
            {"name":"redeploy_weblogic",
             "description":"Redeploy Application",
             "javascript":"getDeployForm('%s', 'weblogic', 'deploy-dialog', 'deploy', '$$filterlist$$')" % settings.BASE_URL,
             "server_operation":"",
             })
        return context_menu_ops
    
    def get_type(self):
        return 'Weblogic'
    
class WeblogicLogContextMenu(ContextOperation):
    
    def get_operations(self):
        context_menu_ops = []
        context_menu_ops.append(
            {"name":"get_log_weblogic",
             "description":"Get Intance Log",
             "javascript":"getLogForm('%s', 'weblogic', 'deploy-dialog', 'get_log', '$$filterlist$$')" % settings.BASE_URL,
             "server_operation":"",
             })
        return context_menu_ops
    
    def get_type(self):
        return 'Weblogic'
    
    
class StartWeblogicInstance(ServerOperation):
    
    def get_visible(self, server):
        agent = server.agents.filter(name='a7xows')
        return len(agent)==1
    
    def get_enabled(self, server):
        return not server.online
    
    def get_name(self):
        return 'Start Weblogic Instance'
    
    def get_image(self):
        return 'start.png'
    
    def request_parameters(self):
        return True
    
    def get_agent(self):
        return 'a7xows'
    
    def get_action(self):
        return 'startinstance'
    
    def get_filter(self, hostname):
        return 'identity_filter=%s' % hostname
    
    def get_url(self, hostname):
        return None
    
    def get_group_name(self):
        return 'WebLogic'
    
    def get_group_icon(self):
        return None
    
class StopWeblogicInstance(ServerOperation):
    
    def get_visible(self, server):
        agent = server.agents.filter(name='a7xows')
        return len(agent)==1
    
    def get_enabled(self, server):
        return not server.online
    
    def get_name(self):
        return 'Stop Weblogic Instance'
    
    def get_image(self):
        return 'stop.png'
    
    def request_parameters(self):
        return True
    
    def get_agent(self):
        return 'a7xows'
    
    def get_action(self):
        return 'stopinstance'
    
    def get_filter(self, hostname):
        return 'identity_filter=%s' % hostname
    
    def get_url(self, hostname):
        return None

    def get_group_name(self):
        return 'WebLogic'
    
    def get_group_icon(self):
        return None
    
    
kermit_modules.register(WeblogicDeployContextMenu)
kermit_modules.register(WeblogicLogContextMenu)

kermit_modules.register(StartWeblogicInstance)
kermit_modules.register(StopWeblogicInstance)