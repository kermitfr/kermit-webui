'''
Created on Aug 11, 2011

@author: mmornati
'''

from django.contrib import admin
from webui.agent.models import Agent, Action, ActionInput, ActionOutput
from guardian.admin import GuardedModelAdmin
    

class AgentAdmin(GuardedModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['name']}),
        ("Details",   {'fields': ['enabled', 'icon']}),         
    ]
    list_display = ('name', 'enabled')
    search_fields = ['name']
    
class ActionAdmin(GuardedModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['name', 'description']}),
        ("Details",   {'fields': ['agent']}),         
    ]
    list_display = ('name', 'description', 'agent')
    search_fields = ['name']

class ActionInputAdmin(GuardedModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['name', 'description']}),
        ("Details",   {'fields': ['type', 'prompt', 'optional', 'validation', 'max_length', 'action']}),         
    ]
    list_display = ('name', 'description', 'action')
    search_fields = ['name']

class ActionOutputAdmin(GuardedModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['name', 'description']}),
        ("Details",   {'fields': ['display_as', 'action']}),         
    ]
    list_display = ('name', 'description', 'action')
    search_fields = ['name']
    
admin.site.register(Agent, AgentAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(ActionInput, ActionInputAdmin)
admin.site.register(ActionOutput, ActionOutputAdmin)
