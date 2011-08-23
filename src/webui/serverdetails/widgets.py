'''
Created on Aug 22, 2011

@author: mmornati
'''
from webui.widgets.base import Widget
import logging
from webui.serverdetails.utils import read_server_info
from django.template.loader import get_template
from django.template.context import Context

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
        
        server_details = read_server_info(args)
        data.update(server_details=server_details)
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
        
        server_details = read_server_info(args)
        data.update(server_details=server_details)
        return template_instance.render(Context(data))
