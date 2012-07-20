'''
Created on Jul 20, 2012

@author: mmornati
'''

from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from webui.dynamicgroups.models import DynaGroup
    

class DynaGroupAdmin(GuardedModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['name']}),
        ("Details",   {'fields': ['engine', 'obj_name', 'rule', 'value']}),         
    ]
    list_display = ('name', 'engine', 'obj_name')
    search_fields = ['name']
    
admin.site.register(DynaGroup, DynaGroupAdmin)
