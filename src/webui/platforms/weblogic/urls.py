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
  
  url(r'^applist/(?P<filters>[\w|\W]+)/(?P<type>[\w|\W]+)/$', 'get_app_list', name = "weblogic_app_list"),
  url(r'^instancelist/(?P<filters>[\w|\W]+)/$', 'get_instance_list', name = "weblogic_instance_list"),
  url(r'^redeploy/(?P<filters>[\w|\W]+)/(?P<dialog_name>[\w|\W]+)/(?P<xhr>.*)', 'redeploy_app', name = "weblogic_redeploy_app"),
  url(r'^get_deploy_form/(?P<dialog_name>[\w|\W]+)/(?P<action>[\w|\W]+)/(?P<filters>[\w|\W]+)/$', 'get_deploy_form', name = "weblogic_get_deploy_form"),
 
  url(r'^get_log_form/(?P<dialog_name>[\w|\W]+)/(?P<action>[\w|\W]+)/(?P<filters>[\w|\W]+)/$', 'get_log_form', name = "weblogic_get_log_form"),
  url(r'^log/(?P<filters>[\w|\W]+)/(?P<dialog_name>[\w|\W]+)/(?P<xhr>.*)', 'get_log', name = "weblogic_get_log"),
  url(r'^get_log_file/(?P<file_name>[\w|\W]+)/$', 'get_log_file', name = "weblogic_get_log_file"),
  
)