'''
Created on Nov 3, 2011

@author: mmornati
'''
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webui.platforms.virtualization.views',
  url(r'^details/(?P<hostname>[\w|\W]+)/(?P<instance_name>[\w|\W]+)/(?P<resource_name>[\w|\W]+)/server/$', 'get_server_details', name = "virtualization_details"),
  
)