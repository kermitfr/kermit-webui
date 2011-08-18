'''
Created on Aug 18, 2011

@author: mmornati
'''

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webui.serverdetails.views',
  #Server Inventory
  url(r'^details/(?P<hostname>[\w|\W]+)/$', 'hostInventory', name = "mcollective-inventory"),
)
