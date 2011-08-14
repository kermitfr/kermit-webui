'''
Created on Aug 12, 2011

@author: mmornati
'''
from automatix.widgets.base import Widget
from automatix.defaultop.models import Operation
from automatix.restserver import views
import logging

logger = logging.getLogger(__name__)

class DashBoardServerStatus(Widget):
    template = "widgets/serverstatus.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        
        try: 
            #TODO: Maybe it's better to call this method with ajax on the panel
            #in this way we can have a loader for the single panel
            #but all other things on the page are ready (or loaded by other calls)
            response, content = views.callRestServer("no-filter", "rpcutil", "ping")
            #TODO: Compare response with database and create dict to shown
        except:
            logger.error("Cannot contact RestServer")
        operations = Operation.objects.filter(enabled=True)
        widget_context = {"operations":operations}
        return dict(super_context.items() + widget_context.items())
