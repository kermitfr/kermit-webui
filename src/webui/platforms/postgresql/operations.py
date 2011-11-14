'''
Created on Nov 8, 2011

@author: mmornati
'''
from webui.abstracts import ContextOperation
from webui import settings
from webui.core import kermit_modules

class PostgreSQLExecuteContextMenu(ContextOperation):
    
    def get_operations(self):
        context_menu_ops = []
        context_menu_ops.append(
            {"name":"execute_sql",
             "description":"PostgreSQL: Execute SQL",
             "javascript":"getSqlExecutionForm('%s', 'postgresql', 'deploy-dialog', 'execute_sql', '$$filterlist$$')" % settings.BASE_URL,
             "server_operation":"",
             })
        return context_menu_ops
    
    def get_type(self):
        return 'SQL'
    
    
kermit_modules.register(PostgreSQLExecuteContextMenu)