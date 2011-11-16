'''
Created on Nov 8, 2011

@author: mmornati
'''
from webui.abstracts import ContextOperation
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
    

kermit_modules.register(OC4JDeployContextMenu)
kermit_modules.register(OC4JGetAppLogContextMenu)