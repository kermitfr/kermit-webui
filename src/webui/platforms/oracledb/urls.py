'''
Created on Nov 3, 2011

@author: mmornati
'''
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webui.platforms.oracledb.views',
  url(r'^details/(?P<hostname>[\w|\W]+)/(?P<database_name>[\w|\W]+)/(?P<resource_name>[\w|\W]+)/server/$', 'get_details', name = "oracledb_details"),
  url(r'^details/(?P<hostname>[\w|\W]+)/(?P<database_name>[\w|\W]+)/(?P<resource_name>[\w|\W]+)/instance/$', 'get_instance_details', name = "oracledb_instance_details"),
 
  url(r'^sql_list/(?P<filters>[\w|\W]+)/$', 'get_sql_list', name = "oracledb_sql_list"),
  url(r'^execute_sql/(?P<filters>[\w|\W]+)/(?P<dialog_name>[\w|\W]+)/(?P<xhr>.*)', 'execute_sql', name = "oracledb_execute_sql"),
  url(r'^get_execute_form/(?P<dialog_name>[\w|\W]+)/(?P<action>[\w|\W]+)/(?P<filters>[\w|\W]+)/$', 'get_execute_form', name = "oracledb_get_sql_execute_form"),
  
  url(r'^get_log_file/(?P<file_name>[\w|\W]+)/$', 'get_log_file', name = "oracledb_get_log_file"),
  
)