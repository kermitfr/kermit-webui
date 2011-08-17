'''
Created on Aug 11, 2011

@author: mmornati
'''

from webui.django_cron.models import Cron, Job
from django.contrib import admin
    

class CronAdmin(admin.ModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['executing']})       
    ]
    list_display = ['executing']
    search_fields = ['executing']
    
class JobAdmin(admin.ModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['name']}),
        ("Details",   {'fields': ['run_frequency', 'last_run', 'instance', 'args', 'kwargs', 'queued']}),         
    ]
    list_display = ('name', 'run_frequency', 'last_run')
    search_fields = ['name']
    
admin.site.register(Cron, CronAdmin)
admin.site.register(Job, JobAdmin)