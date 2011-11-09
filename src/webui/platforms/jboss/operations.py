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
             "description":"Deploy App on JBoss",
             "javascript":"getDeployForm('%s', 'jboss', 'deploy-dialog', 'deploy', '$$filterlist$$')" % settings.BASE_URL,
             "server_operation":"",
             })
        return context_menu_ops
    
    def get_type(self):
        return 'Deploy App'
    
    
kermit_modules.register(JbossDeployContextMenu)