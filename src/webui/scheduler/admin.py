'''
Created on Aug 11, 2011

@author: mmornati
'''

from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from webui.scheduler.models import TaskScheduler
    

class SchedulerAdmin(GuardedModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['periodic_task']}),
        ("Details",   {'fields': []}),         
    ]
    list_display = ('periodic_task',)
    search_fields = ['periodic_task']
    
admin.site.register(TaskScheduler, SchedulerAdmin)
