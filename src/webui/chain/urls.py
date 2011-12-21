'''
Created on Nov 17, 2011

@author: mmornati
'''
from django.conf.urls.defaults import *


urlpatterns = patterns('webui.chain.views',
    url(r'^show/$', 'show_page', name='chain_show_page'),
    url(r'^serverlist/$', 'server_list', name='chain_server_list'),
    url(r'^execute/(?P<xhr>.*)', 'execute_chain', name='chain_execute'),
    
    url(r'^sql_list/(?P<servers>[\w|\W]+)/$', 'get_sql_list', name='chain_sql_list'),
    url(r'^ear_list/(?P<servers>[\w|\W]+)/(?P<server_type>[\w|\W]+)/$', 'get_app_list', name = "chain_app_list"),
    url(r'^bar_list/(?P<servers>[\w|\W]+)/$', 'get_bar_list', name = "chain_bar_list"),
  
)