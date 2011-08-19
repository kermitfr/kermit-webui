'''
Created on Aug 11, 2011

@author: mmornati
'''

from webui.widgets.models import Widget
from django.contrib import admin

class WidgetAdmin(admin.ModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['name']}),
        ("Details",   {'fields': ['title', 'description', 'enabled', 'icon', 'color', 'column', 'order', 'movable', 'removable', 'editable', 'refreshable', 'refreshUrl']}),         
    ]
    list_display = ('name', 'title')
    search_fields = ['name']
    
admin.site.register(Widget, WidgetAdmin)