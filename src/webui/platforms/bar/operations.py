'''
Created on Nov 8, 2011

@author: mmornati
'''
from webui.abstracts import ContextOperation
from webui import settings
from webui.core import kermit_modules

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
    

kermit_modules.register(BarDeployContextMenu)
