'''
Created on Nov 8, 2011

@author: mmornati
'''
from webui.abstracts import ContextOperation
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
    
    
kermit_modules.register(WeblogicDeployContextMenu)