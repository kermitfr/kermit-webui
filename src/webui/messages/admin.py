'''
Created on Aug 11, 2011

@author: mmornati
'''

from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from webui.messages.models import Message, IgnoredMessage
    

class MessageAdmin(GuardedModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['level', 'server', 'time']}),
        ("Details",   {'fields': ['message']}),         
    ]
    list_display = ('level', 'server', 'time', 'message')
    search_fields = ['level', 'server']
    
class IgnoredMessageAdmin(GuardedModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['server', 'message']}),
        ("Details",   {'fields': []}),         
    ]
    list_display = ('server', 'message')
    search_fields = ['server', 'message']
    
admin.site.register(Message, MessageAdmin)
admin.site.register(IgnoredMessage, IgnoredMessageAdmin)
