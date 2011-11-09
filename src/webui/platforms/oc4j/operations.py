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
             "description":"Redeploy App on OC4J",
             "javascript":"getDeployForm('%s', 'oc4j', 'deploy-dialog', 'deploy', '$$filterlist$$')" % settings.BASE_URL,
             "server_operation":"",
             })
        return context_menu_ops
    
    def get_type(self):
        return 'Deploy App'
    
    
kermit_modules.register(OC4JDeployContextMenu)