'''
Created on Aug 10, 2011

@author: mmornati
'''

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webui.sqldeploy.views',
  #Response without templating
  url(r'^sqllist/(?P<filters>[\w|\W]+)/$', 'get_sql_list', name = "sql_list"),
  url(r'^redeploy/(?P<filters>[\w|\W]+)/(?P<dialog_name>[\w|\W]+)/(?P<xhr>.*)', 'redeploy_sql', name = "redeploy_sql"),
  url(r'^get_deploy_form/(?P<dialog_name>[\w|\W]+)/(?P<action>[\w|\W]+)/(?P<filters>[\w|\W]+)/$', 'get_deploy_form', name = "get_sql_deploy_form"),
 
  
)
