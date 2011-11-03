'''
Created on Aug 18, 2011

@author: mmornati
'''

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webui.platforms.bar.views',
  url(r'^details/(?P<hostname>[\w|\W]+)/(?P<console_name>[\w|\W]+)/(?P<resource_name>[\w|\W]+)/pools/$', 'poolsInventory', name = "bar_pools_details"),
  url(r'^details/(?P<hostname>[\w|\W]+)/(?P<console_name>[\w|\W]+)/(?P<resource_name>[\w|\W]+)/pool/$', 'poolInventory', name = "bar_pool_details"),
  url(r'^details/(?P<hostname>[\w|\W]+)/(?P<console_name>[\w|\W]+)/(?P<resource_name>[\w|\W]+)/bar/$', 'barInventory', name = "bar_details"),
  url(r'^details/(?P<hostname>[\w|\W]+)/(?P<console_name>[\w|\W]+)/(?P<resource_name>[\w|\W]+)/console/$', 'barConsoleInventory', name = "bar_console_details"),
)