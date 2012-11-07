'''
Created on Aug 22, 2011

@author: mmornati
'''
from webui.widgets.base import Widget
import logging
from django.template.loader import get_template
from django.template.context import Context
from webui.servers.models import Server
from webui.puppetclasses.models import PuppetClass
from webui.servers import utils

logger = logging.getLogger(__name__)

class ServerDetails(Widget):
    template = "widgets/servers/serverdetails.html"
    
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
    template = "widgets/servers/resourcedetails.html"
    
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
    template = "widgets/servers/summary.html"
    
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
    
class ServerEdit(Widget):
    template = "widgets/servers/editserver.html"
    
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
            my_server=servers[0]
            data.update(server=my_server)
            assigned_classes = []
            if my_server and my_server.puppet_classes:
                for current_class in my_server.puppet_classes.order_by('name').all():
                    assigned_classes.append(current_class)
            data.update(server_classes=assigned_classes)
        assignable_classes = PuppetClass.objects.all().order_by('name')
        available_classes = list(set(assignable_classes) - set(assigned_classes))
        data.update(available_classes=available_classes)
        return template_instance.render(Context(data))

class SystemStatus(Widget):
    template = "widgets/servers/systemstatus.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        servers = utils.extract_user_servers(self.user)
        
        widget_context = {"servers":servers}
        return dict(super_context.items() + widget_context.items())
    
class ServerStatus(Widget):
    template = "widgets/servers/serverstatus.html"
    
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
                    if "lvl5" in serverdict:
                        serverdict["lvl5"]=serverdict["lvl5"] + ', ' + puppetclass["name"]
                    else:    
                        serverdict["lvl5"]=puppetclass["name"]
            serverslist.append(serverdict)
        widget_context = {"servers":serverslist}
        return dict(super_context.items() + widget_context.items())
