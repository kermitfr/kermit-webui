'''
Created on Aug 12, 2011

@author: mmornati
'''
from webui.widgets.base import Widget
import logging
from webui.chain.models import Scheduler
from django.utils import simplejson as json
from webui.serverstatus.models import Server
from webui import settings
from guardian.shortcuts import get_objects_for_user

logger = logging.getLogger(__name__)

class ChainHistory(Widget):
    template = "widgets/chain/chain_history.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        if not self.user.is_superuser:
            logger.debug("Loading just user %s schedulers" % self.user)
            scheds = Scheduler.objects.filter(user=self.user)
        else:
            logger.debug("Admin user: loading all users scheduled operations")
            scheds = Scheduler.objects.all()
            
        logger.info("Composing sched_information information")
        scheds_list = []
        for scheduler in scheds:
            scheduler_obj = {"user": scheduler.user,
                       "name": scheduler.name,
                       "last_run": scheduler.last_run,
                       "task_running": scheduler.task_running,
                       "status": scheduler.status
                       }
            scheds_list.append(scheduler_obj)
        
        widget_context = {"schedulers":scheds_list}
        return dict(super_context.items() + widget_context.items())
    
class ChainEditor(Widget):
    template = "widgets/chain/chain_editor.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        operations = [{'id': 'script_ex', 'name': 'Execute Script'},
                  {'id': 'deploy_bar', 'name': 'Deploy Bar'},
                  {'id': 'deploy_ear', 'name': 'Deploy EAR'},
                  {'id': 'restart_instance', 'name': 'Restart Instance'}]
    
        servers = Server.objects.filter(deleted=False)
        if not self.user.is_superuser and settings.FILTERS_SERVER:
            servers = get_objects_for_user(self.user, 'use_server', Server).filter(deleted=False)
        server_list = []
        for server in servers:
            server_list.append({'id': server.fqdn, 'name': server.fqdn})
        
        server_dict = {"results": server_list, "total": len(server_list)}
        widget_context = {'operations': operations, 'server_list':json.dumps(server_dict, ensure_ascii=False)}
        return dict(super_context.items() + widget_context.items())
