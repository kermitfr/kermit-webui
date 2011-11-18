'''
Created on Nov 15, 2011

@author: mmornati
'''
from webui.abstracts import ServerOperation
from django.core.urlresolvers import reverse

class StartServer(ServerOperation):
    
    def get_visible(self):
        return True
    
    def get_enabled(self, server):
        return not server.online
    
    def get_name(self):
        return 'Start Server'
    
    def get_image(self):
        return 'start.png'
    
    def get_url(self, hostname):
        return reverse('call_mcollective', kwargs={'filters':'identity_filter=%s'%hostname, 'agent':'rpcutil', 'action':'ping'})
    

class StopServer(ServerOperation):
    
    def get_visible(self):
        return True
    
    def get_enabled(self, server):
        return server.online
    
    def get_name(self):
        return 'Stop Server'
    
    def get_image(self):
        return 'stop.png'
    
    def get_url(self, hostname):
        return reverse('call_mcollective', kwargs={'filters':'identity_filter=%s'%hostname, 'agent':'rpcutil', 'action':'ping'})
    
#kermit_modules.register(StartServer)
#kermit_modules.register(StopServer)