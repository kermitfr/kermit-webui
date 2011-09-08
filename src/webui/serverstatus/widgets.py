'''
Created on Aug 12, 2011

@author: mmornati
'''
from webui.widgets.base import Widget
import logging
from webui.serverstatus.models import Server
from guardian.shortcuts import get_objects_for_user

logger = logging.getLogger(__name__)

class DashBoardServerStatus(Widget):
    template = "widgets/serverstatus/serverstatus.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        servers = Server.objects.filter(deleted=False)
        if self.user != 'fooUser':
            if not self.user.is_superuser:
                servers = get_objects_for_user(self.user, 'use_server', Server)
        
        widget_context = {"servers":servers}
        return dict(super_context.items() + widget_context.items())
