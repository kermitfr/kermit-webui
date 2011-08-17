'''
Created on Aug 11, 2011

@author: mmornati
'''

from webui.puppetclasses.models import PuppetClass
from django.contrib import admin
    

class PuppetClassAdmin(admin.ModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['name']}),
        ("Details",   {'fields': ['description', 'icon', 'enabled', 'parent']}),         
    ]
    list_display = ('name', 'description')
    search_fields = ['name']
    
admin.site.register(PuppetClass, PuppetClassAdmin)
