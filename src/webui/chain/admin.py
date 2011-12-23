'''
Created on Dec 22, 2011

@author: mmornati
'''

from django.contrib import admin
from webui.chain.models import Scheduler, SchedulerTask

class SchedulerAdmin(admin.ModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['name']}),
        ("Details",   {'fields': ['user', 'last_run', 'task_running', 'status', 'task_uuid']}),         
    ]
    list_display = ('user', 'task_running', 'status')
    search_fields = ['user']
    
class SchedulerTaskAdmin(admin.ModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['order', 'name', 'scheduler']}),
        ("Details",   {'fields': ['agent', 'action', 'parameters', 'filters', 'run_at', 'result']}),         
    ]
    list_display = ('scheduler', 'name', 'agent', 'action', 'parameters', 'filters', 'run_at', 'result')
    search_fields = ['user']
    
    
admin.site.register(Scheduler, SchedulerAdmin)
admin.site.register(SchedulerTask, SchedulerTaskAdmin)