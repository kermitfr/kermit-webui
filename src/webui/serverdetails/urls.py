'''
Created on Aug 18, 2011

@author: mmornati
'''

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webui.serverdetails.views',
  url(r'^details/(?P<hostname>[\w|\W]+)/(?P<instance_name>[\w|\W]+)/(?P<resource_name>[\w|\W]+)/instance/$', 'instanceInventory', name = "mcollective-inventory"),
  url(r'^details/(?P<hostname>[\w|\W]+)/(?P<instance_name>[\w|\W]+)/(?P<resource_name>[\w|\W]+)/datasources/$', 'datasourceListInventory', name = "mcollective-inventory"),
  url(r'^details/(?P<hostname>[\w|\W]+)/(?P<instance_name>[\w|\W]+)/(?P<resource_name>[\w|\W]+)/datasource/$', 'datasourceInventory', name = "mcollective-inventory"),
  url(r'^details/(?P<hostname>[\w|\W]+)/(?P<instance_name>[\w|\W]+)/(?P<resource_name>[\w|\W]+)/application/$', 'applicationInventory', name = "mcollective-inventory"),
  #Server Inventory
  url(r'^details/(?P<hostname>[\w|\W]+)/$', 'hostInventory', name = "mcollective-inventory"),
  url(r'^tree/(?P<hostname>[\w|\W]+)/$', 'getDetailsTree', name = "mcollective-inventory"),
)
