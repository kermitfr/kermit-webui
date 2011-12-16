'''
Created on Nov 8, 2011

@author: mmornati
'''
from webui.abstracts import ContextOperation, ServerOperation
from webui import settings
from webui.core import kermit_modules
from guardian.shortcuts import get_objects_for_user
from webui.agent.models import Agent, Action

class OC4JReDeployContextMenu(ContextOperation):
    
    def get_operations(self):
        context_menu_ops = []
        context_menu_ops.append(
            {"name":"redeploy_OC4J",
             "description":"Redeploy Application",
             "javascript":"getDeployForm('%s', 'oc4j', 'deploy-dialog', 'redeploy', '$$filterlist$$')" % settings.BASE_URL,
             "server_operation":"",
             })
        return context_menu_ops
    
    def get_type(self):
        return 'OC4J'
    
    def get_visible(self, server):
        agent = server.agents.filter(name='a7xoas')
        classes = server.puppet_classes.filter(name='oas')
        return len(agent)==1 and len(classes)==1
    
    def get_enabled(self, user):
        if not user.is_superuser:
            agents = get_objects_for_user(user, 'use_agent', Agent).filter(enabled=True, name="a7xoas")
            if len(agents)==1:
                action = get_objects_for_user(user, 'use_action', Action).filter(agent=agents[0], name="redeploy")
                return action and len(action)==1
            else:
                return False
        else:
            return True
    
class OC4JCreateInstanceContextMenu(ContextOperation):
    
    def get_operations(self):
        context_menu_ops = []
        context_menu_ops.append(
            {"name":"create_instace_oc4j",
             "description":"Create Instance",
             "javascript":"getForm('%s', 'oc4j', 'deploy-dialog', 'createinstance', '$$filterlist$$')" % settings.BASE_URL,
             "server_operation":"",
             })
        return context_menu_ops
    
    def get_type(self):
        return 'OC4J'
    
    def get_visible(self, server):
        agent = server.agents.filter(name='a7xoas')
        classes = server.puppet_classes.filter(name='oas')
        return len(agent)==1 and len(classes)==1
    
    def get_enabled(self, user):
        if not user.is_superuser:
            agents = get_objects_for_user(user, 'use_agent', Agent).filter(enabled=True, name="a7xoas")
            if len(agents)==1:
                action = get_objects_for_user(user, 'use_action', Action).filter(agent=agents[0], name="createinstance")
                return action and len(action)==1
            else:
                return False
        else:
            return True
    
class OC4JAddPoolContextMenu(ContextOperation):
    
    def get_operations(self):
        context_menu_ops = []
        context_menu_ops.append(
            {"name":"add_pool_oc4j",
             "description":"Add Pool",
             "javascript":"getForm('%s', 'oc4j', 'deploy-dialog', 'addpool', '$$filterlist$$')" % settings.BASE_URL,
             "server_operation":"",
             })
        return context_menu_ops
    
    def get_type(self):
        return 'OC4J'
    
    def get_visible(self, server):
        agent = server.agents.filter(name='a7xoas')
        classes = server.puppet_classes.filter(name='oas')
        return len(agent)==1 and len(classes)==1
    
    def get_enabled(self, user):
        if not user.is_superuser:
            agents = get_objects_for_user(user, 'use_agent', Agent).filter(enabled=True, name="a7xoas")
            if len(agents)==1:
                action = get_objects_for_user(user, 'use_action', Action).filter(agent=agents[0], name="add_pool")
                return action and len(action)==1
            else:
                return False
        else:
            return True
    
class OC4JDeployContextMenu(ContextOperation):
    
    def get_operations(self):
        context_menu_ops = []
        context_menu_ops.append(
            {"name":"deploy_OC4J",
             "description":"Deploy Application",
             "javascript":"getDeployForm('%s', 'oc4j', 'deploy-dialog', 'deploy', '$$filterlist$$')" % settings.BASE_URL,
             "server_operation":"",
             })
        return context_menu_ops
    
    def get_type(self):
        return 'OC4J'
    
    def get_visible(self, server):
        agent = server.agents.filter(name='a7xoas')
        classes = server.puppet_classes.filter(name='oas')
        return len(agent)==1 and len(classes)==1
    
    def get_enabled(self, user):
        if not user.is_superuser:
            agents = get_objects_for_user(user, 'use_agent', Agent).filter(enabled=True, name="a7xoas")
            if len(agents)==1:
                action = get_objects_for_user(user, 'use_action', Action).filter(agent=agents[0], name="deploy")
                return action and len(action)==1
            else:
                return False
        else:
            return True
    
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
    
    def get_visible(self, server):
        agent = server.agents.filter(name='a7xoas')
        classes = server.puppet_classes.filter(name='oas')
        return len(agent)==1 and len(classes)==1
    
    def get_enabled(self, user):
        if not user.is_superuser:
            agents = get_objects_for_user(user, 'use_agent', Agent).filter(enabled=True, name="a7xoas")
            if len(agents)==1:
                action = get_objects_for_user(user, 'use_action', Action).filter(agent=agents[0], name="get_log")
                return action and len(action)==1
            else:
                return False
        else:
            return True
    
class StartOC4JInstance(ServerOperation):
    
    def get_visible(self, server, user):
        agent = server.agents.filter(name='a7xoas')
        classes = server.puppet_classes.filter(name='oas')
        if len(agent)==1 and len(classes)==1:
            if not user.is_superuser:
                agents = get_objects_for_user(user, 'use_agent', Agent).filter(enabled=True, name="a7xoas")
                if len(agents)==1:
                    action = get_objects_for_user(user, 'use_action', Action).filter(agent=agents[0], name="startinstance")
                    return action and len(action)==1
                else:
                    return False
            else:
                return True
        else:
            return False
    
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
    
    def get_visible(self, server, user):
        agent = server.agents.filter(name='a7xoas')
        classes = server.puppet_classes.filter(name='oas')
        if len(agent)==1 and len(classes)==1:
            if not user.is_superuser:
                agents = get_objects_for_user(user, 'use_agent', Agent).filter(enabled=True, name="a7xoas")
                if len(agents)==1:
                    action = get_objects_for_user(user, 'use_action', Action).filter(agent=agents[0], name="stoptinstance")
                    return action and len(action)==1
                else:
                    return False
            else:
                return True
        else:
            return False
    
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
kermit_modules.register(OC4JReDeployContextMenu)
kermit_modules.register(OC4JCreateInstanceContextMenu)
kermit_modules.register(OC4JGetAppLogContextMenu)
kermit_modules.register(OC4JAddPoolContextMenu)

kermit_modules.register(StartOC4JInstance)
kermit_modules.register(StopOC4JInstance)