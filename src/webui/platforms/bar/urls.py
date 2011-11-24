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
  
  url(r'^get_deploy_form/(?P<dialog_name>[\w|\W]+)/(?P<action>[\w|\W]+)/(?P<filters>[\w|\W]+)/$', 'get_deploy_form', name = "bar_get_deploy_form"),
  url(r'^barlist/(?P<filters>[\w|\W]+)/$', 'get_bar_list', name = "bar_list"),
  url(r'^deploy/(?P<filters>[\w|\W]+)/(?P<dialog_name>[\w|\W]+)/(?P<xhr>.*)', 'deploy_bar', name = "bar_deploy"),
)