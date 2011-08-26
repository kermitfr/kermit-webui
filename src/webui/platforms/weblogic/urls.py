'''
Created on Aug 18, 2011

@author: mmornati
'''

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webui.platforms.weblogic.views',
  url(r'^details/(?P<hostname>[\w|\W]+)/(?P<resource_name>[\w|\W]+)/instance/$', 'instanceInventory', name = "weblogic_instance_details"),
  url(r'^details/(?P<hostname>[\w|\W]+)/(?P<resource_name>[\w|\W]+)/datasource/$', 'datasourceInventory', name = "weblogic_datasource_details"),
  url(r'^details/(?P<hostname>[\w|\W]+)/(?P<resource_name>[\w|\W]+)/nodemanager/$', 'nodeManagerInventory', name = "weblogic_nodemanager_details"),
  url(r'^details/(?P<hostname>[\w|\W]+)/(?P<resource_name>[\w|\W]+)/console/$', 'consoleInventory', name = "weblogic_console_details"),
  url(r'^details/(?P<hostname>[\w|\W]+)/(?P<resource_name>[\w|\W]+)/application/$', 'applicationInventory', name = "weblogic_application_details"),
)