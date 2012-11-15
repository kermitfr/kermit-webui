'''
Created on Nov 7, 2012

@author: mmornati
'''
from webui.abstracts import ServerOperation
from webui.core import kermit_modules
from django.core.urlresolvers import reverse

class OVirtCreateVM(ServerOperation):
    
    def get_visible(self, server, user):
        agent = server.agents.filter(name='ovirt')
        return len(agent)==1
    
    def get_enabled(self, server):
        return not server.online
    
    def get_name(self):
        return 'Create VM'
    
    def get_group_name(self):
        return 'Virtualization'
    
    def get_image(self):
        return 'virtualization.png'
    
    def is_mcollective(self):
        return False
    
    def get_url(self, hostname, instancename=None):
        return reverse('ovirt_create_vm', kwargs={'hostname':hostname})
    
    
kermit_modules.register(OVirtCreateVM)