'''
Created on Aug 11, 2011

@author: mmornati
'''

from webui.serverstatus.models import Server
from django.contrib import admin
from guardian.admin import GuardedModelAdmin
    

class ServerAdmin(GuardedModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['hostname', 'fqdn']}),
        ("Details",   {'fields': ['os', 'architecture', 'deleted', 'icon', 'puppet_classes', 'agents', 'online', 'puppet_path']}),         
    ]
    list_display = ('hostname', 'fqdn', 'os', 'architecture')
    search_fields = ['hostname']
    
admin.site.register(Server, ServerAdmin)
