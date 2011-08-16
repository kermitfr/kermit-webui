from webui.index.models import Menu
from django.contrib import admin


class MenuAdmin(admin.ModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['name', 'url', 'order', 'enabled']}),
    ]
    list_display = ('name', 'url', 'order', 'enabled')
    search_fields = ['name', 'url']
    list_filter = ['enabled']
    
    
admin.site.register(Menu, MenuAdmin)
