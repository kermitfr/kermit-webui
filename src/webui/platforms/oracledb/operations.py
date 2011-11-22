'''
Created on Nov 8, 2011

@author: mmornati
'''
from webui.abstracts import ContextOperation
from webui import settings
from webui.core import kermit_modules

class OracleDBxecuteContextMenu(ContextOperation):
    
    def get_operations(self):
        context_menu_ops = []
        context_menu_ops.append(
            {"name":"execute_sql",
             "description":"Execute SQL",
             "javascript":"getSqlExecutionForm('%s', 'oracledb', 'deploy-dialog', 'execute_sql', '$$filterlist$$')" % settings.BASE_URL,
             "server_operation":"",
             })
        return context_menu_ops
    
    def get_type(self):
        return 'OracleDB'
    
    
kermit_modules.register(OracleDBxecuteContextMenu)