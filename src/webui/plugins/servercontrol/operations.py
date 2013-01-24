'''
Created on Nov 15, 2011

@author: mmornati
'''
from webui.abstracts import ServerOperation
from django.core.urlresolvers import reverse
from webui.core import kermit_modules

class StartServer(ServerOperation):
    
    def get_visible(self, server, user):
        return not server.online
    
    def get_enabled(self, server):
        return not server.online
    
    def get_name(self):
        return 'Start Server'
    
    def get_group_name(self):
        return 'Server Control'
    
    def get_image(self):
        return 'start.png'
    
    def get_url(self, hostname, instancename=None):
        return reverse('call_mcollective_with_arguments', kwargs={'wait_for_response':'True'})
    
    def get_agent(self):
        return 'rpcutil'
    
    def get_action(self):
        return 'ping'
    
    def get_filter(self, hostname):
        return 'identity=%s'%hostname
    
class StopServer(ServerOperation):
    
    def get_visible(self, server, user):
        return server.online
    
    def get_enabled(self, server):
        return server.online
    
    def get_name(self):
        return 'Stop Server'
    
    def get_group_name(self):
        return 'Server Control'
    
    def get_image(self):
        return 'stop.png'
    
    def get_url(self, hostname, instancename=None):
        return reverse('call_mcollective')
    
    def get_agent(self):
        return 'system'
    
    def get_action(self):
        return 'halt'
    
    def get_filter(self, hostname):
        return 'identity=%s'%hostname
    
kermit_modules.register(StartServer)
kermit_modules.register(StopServer)