'''
Created on Nov 8, 2011

@author: mmornati
'''
from webui.abstracts import ContextOperation, ServerOperation
from webui import settings
from webui.core import kermit_modules

class OC4JDeployContextMenu(ContextOperation):
    
    def get_operations(self):
        context_menu_ops = []
        context_menu_ops.append(
            {"name":"redeploy_OC4J",
             "description":"Redeploy Application",
             "javascript":"getDeployForm('%s', 'oc4j', 'deploy-dialog', 'deploy', '$$filterlist$$')" % settings.BASE_URL,
             "server_operation":"",
             })
        return context_menu_ops
    
    def get_type(self):
        return 'OC4J'
    
class OC4JGetAppLogContextMenu(ContextOperation):
    
    def get_operations(self):
        context_menu_ops = []
        context_menu_ops.append(
            {"name":"get_log_form_OC4J",
             "description":"Get Application Log",
             "javascript":"getLogForm('%s', 'oc4j', 'deploy-dialog', 'get_log', '$$filterlist$$')" % settings.BASE_URL,
             "server_operation":"",
             })
        return context_menu_ops
    
    def get_type(self):
        return 'OC4J'
    
class StartOC4JInstance(ServerOperation):
    
    def get_visible(self, server):
        agent = server.agents.filter(name='a7xoas')
        return len(agent)==1
    
    def get_enabled(self, server):
        return not server.online
    
    def get_name(self):
        return 'Start OC4J Instance'
    
    def get_image(self):
        return 'start.png'
    
    def request_parameters(self):
        return True
    
    def get_agent(self):
        return 'a7xoas'
    
    def get_action(self):
        return 'startinstance'
    
    def get_filter(self, hostname):
        return 'identity_filter=%s' % hostname
    
    def get_url(self, hostname):
        return None
    
    def get_group_name(self):
        return 'OC4J'
    
    def get_group_icon(self):
        return None
    
class StopOC4JInstance(ServerOperation):
    
    def get_visible(self, server):
        agent = server.agents.filter(name='a7xoas')
        return len(agent)==1
    
    def get_enabled(self, server):
        return not server.online
    
    def get_name(self):
        return 'Stop OC4J Instance'
    
    def get_image(self):
        return 'stop.png'
    
    def request_parameters(self):
        return True
    
    def get_agent(self):
        return 'a7xoas'
    
    def get_action(self):
        return 'stopinstance'
    
    def get_filter(self, hostname):
        return 'identity_filter=%s' % hostname
    
    def get_url(self, hostname):
        return None
    
    def get_group_name(self):
        return 'OC4J'
    
    def get_group_icon(self):
        return None

kermit_modules.register(OC4JDeployContextMenu)
kermit_modules.register(OC4JGetAppLogContextMenu)

kermit_modules.register(StartOC4JInstance)
kermit_modules.register(StopOC4JInstance)