'''
Created on Nov 3, 2011

@author: mmornati
'''
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webui.platforms.jboss.views',
  url(r'^details/(?P<hostname>[\w|\W]+)/(?P<instance_name>[\w|\W]+)/(?P<resource_name>[\w|\W]+)/server/$', 'jboss_details', name = "jboss_details"),
  
  url(r'^applist/(?P<filters>[\w|\W]+)/(?P<type>[\w|\W]+)/$', 'get_app_list', name = "jboss_app_list"),
  url(r'^instancelist/(?P<filters>[\w|\W]+)/$', 'get_instance_list', name = "jboss_instance_list"),
  url(r'^redeploy/(?P<filters>[\w|\W]+)/(?P<dialog_name>[\w|\W]+)/(?P<xhr>.*)', 'redeploy_app', name = "jboss_redeploy_app"),
  url(r'^get_deploy_form/(?P<dialog_name>[\w|\W]+)/(?P<action>[\w|\W]+)/(?P<filters>[\w|\W]+)/$', 'get_deploy_form', name = "jboss_get_deploy_form"),
 
)