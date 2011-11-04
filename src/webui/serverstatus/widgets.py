'''
Created on Aug 12, 2011

@author: mmornati
'''
from webui.widgets.base import Widget
import logging
from webui.serverdetails import utils

logger = logging.getLogger(__name__)

class SystemStatus(Widget):
    template = "widgets/serverstatus/systemstatus.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        servers = utils.extract_user_servers(self.user)
        
        widget_context = {"servers":servers}
        return dict(super_context.items() + widget_context.items())
    
class ServerStatus(Widget):
    template = "widgets/serverstatus/serverstatus.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        servers = utils.extract_user_servers(self.user)
        #Extracting puppet classes level
        serverslist=[]
        for server in servers:
            serverdict = {}
            serverdict["online"]=server.online
            serverdict["fqdn"]=server.fqdn
            serverdict["hostname"]=server.hostname
            for puppetclass in server.puppet_classes.values():
                if puppetclass["level"]==0:
                    serverdict["lvl1"]=puppetclass["name"]
                elif puppetclass["level"]==1:
                    serverdict["lvl2"]=puppetclass["name"]
                elif puppetclass["level"]==2:
                    serverdict["lvl3"]=puppetclass["name"]
                elif puppetclass["level"]==3:
                    serverdict["lvl4"]=puppetclass["name"]
                elif puppetclass["level"]==4:
                    serverdict["lvl5"]=puppetclass["name"]
            serverslist.append(serverdict)
        widget_context = {"servers":serverslist}
        return dict(super_context.items() + widget_context.items())
