'''
Created on Sep 20, 2011

@author: mmornati
'''
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webui.exporter.views',
    url(r'^servers/csv/$', 'export_servers_csv', name="export_servers_csv"),
    url(r'^servers/xls/$', 'export_servers_xls', name="export_servers_xls"),
)

