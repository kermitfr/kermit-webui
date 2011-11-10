'''
Created on Nov 3, 2011

@author: mmornati
'''
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webui.platforms.postgresql.views',
  url(r'^details/(?P<hostname>[\w|\W]+)/(?P<database_name>[\w|\W]+)/(?P<resource_name>[\w|\W]+)/pgsql/$', 'get_details', name = "postgres_details"),
  url(r'^details/(?P<hostname>[\w|\W]+)/(?P<database_name>[\w|\W]+)/(?P<resource_name>[\w|\W]+)/pgdatabase/$', 'get_db_details', name = "postgres_db_details"),
  
)