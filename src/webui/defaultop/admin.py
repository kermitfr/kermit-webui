'''
Created on Aug 11, 2011

@author: mmornati
'''

from webui.defaultop.models import Operation
from django.contrib import admin
from guardian.admin import GuardedModelAdmin
    

class OperationAdmin(GuardedModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['name']}),
        ("Details",   {'fields': ['description', 'icon', 'url', 'enabled', 'with_template']}),         
    ]
    list_display = ('name', 'url')
    search_fields = ['name']
    
admin.site.register(Operation, OperationAdmin)