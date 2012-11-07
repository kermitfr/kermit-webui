'''
Created on Nov 7, 2012

@author: mmornati
'''
from webui.abstracts import ServerOperation
from webui.core import kermit_modules
from django.core.urlresolvers import reverse

class EditServerClasses(ServerOperation):
    
    def get_visible(self, server, user):
        return True
    
    def get_enabled(self, server):
        return not server.online
    
    def get_name(self):
        return 'Edit Server Classes'
    
    def get_group_name(self):
        return 'Edit Server'
    
    def get_image(self):
        return 'edit.png'
    
    def is_mcollective(self):
        return False
    
    def get_url(self, hostname, instancename=None):
        return reverse('editserver', kwargs={'hostname':hostname})
    
    
kermit_modules.register(EditServerClasses)