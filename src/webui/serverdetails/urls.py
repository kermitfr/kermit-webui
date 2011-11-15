'''
Created on Aug 18, 2011

@author: mmornati
'''

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webui.serverdetails.views',
  url(r'^tree/(?P<hostname>[\w|\W]+)/$', 'getDetailsTree', name = "serverdetailstree"),
  url(r'^details/(?P<hostname>[\w|\W]+)/$', 'hostInventory', name = "serverdetails"),
  
  url(r'^detailsinv/(?P<hostname>[\w|\W]+)/$', 'hostCallInventory', name = "server_inventory_details"),
)
