'''
Created on Aug 22, 2011

@author: mmornati
'''
from webui.widgets.base import Widget
import logging
from django.template.loader import get_template
from django.template.context import Context
from webui.serverstatus.models import Server

logger = logging.getLogger(__name__)

class ServerDetails(Widget):
    template = "widgets/serverdetails/serverdetails.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        return dict(super_context.items())
    
    def render(self, args):
        logger.debug('Calling override render for ' + __name__)
        template_instance = get_template(self.template)
        data = self.get_context()
        data.update(widget=self, user=self.user, hostname=args)
        
#        server_details = read_server_info(args)
#        data.update(server_details=server_details)
        return template_instance.render(Context(data))
    
class SelectedResourceDetails(Widget):
    template = "widgets/serverdetails/resourcedetails.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        return dict(super_context.items())
    
    def render(self, args):
        logger.debug('Calling override render for ' + __name__)
        template_instance = get_template(self.template)
        data = self.get_context()
        data.update(widget=self, user=self.user, hostname=args)
        
#        server_details = read_server_info(args)
#        data.update(server_details=server_details)
        return template_instance.render(Context(data))
    
class ServerSummary(Widget):
    template = "widgets/serverdetails/summary.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        return dict(super_context.items())
    
    def render(self, args):
        logger.debug('Calling override render for ' + __name__)
        template_instance = get_template(self.template)
        data = self.get_context()
        data.update(widget=self, user=self.user, hostname=args)
        
        servers = Server.objects.filter(deleted=False, hostname=args)
        if len(servers)>0:
            data.update(server=servers[0])
        return template_instance.render(Context(data))

