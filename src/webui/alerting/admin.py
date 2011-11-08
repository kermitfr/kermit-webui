'''
Created on Aug 11, 2011

@author: mmornati
'''

from django.contrib import admin

from webui.alerting.models import Alert, Event

class AlertAdmin(admin.ModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['name', 'enabled']}),
        ("Details",   {'fields': ['module', 'description', 'users', 'run_frequency', 'last_run', 'event', 'template']})       
    ]
    list_display = ['name', 'enabled']
    search_fields = ['name', 'enabled']
    
class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['name']}),
        ("Details",   {'fields': ['description', 'object_pk']}) 
    ]
    list_display = ['name']
    search_fields = ['name']
    
    
admin.site.register(Alert, AlertAdmin)
admin.site.register(Event, EventAdmin)
