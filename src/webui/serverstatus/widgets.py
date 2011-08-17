'''
Created on Aug 12, 2011

@author: mmornati
'''
from webui.widgets.base import Widget
from webui.restserver import views
import logging
from webui.serverstatus.models import Server

logger = logging.getLogger(__name__)

class DashBoardServerStatus(Widget):
    template = "widgets/serverstatus.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        
        servers = Server.objects.filter(deleted=False)
        widget_context = {"servers":servers}
        return dict(super_context.items() + widget_context.items())
