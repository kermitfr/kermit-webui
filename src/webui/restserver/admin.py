'''
Created on Dec 22, 2011

@author: mmornati
'''

from django.contrib import admin
from webui.restserver.models import BackendJob

class BackendJobAdmin(admin.ModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['user', 'run_at']}),
        ("Details",   {'fields': ['task_uuid']}),         
    ]
    list_display = ('user', 'run_at', 'task_uuid')
    search_fields = ['user']
    
admin.site.register(BackendJob, BackendJobAdmin)
