'''
Created on Aug 10, 2011

@author: mmornati
'''

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('automatix.restserver.views',
  url(r'^mcollective/(?P<filters>[\w|\W]+)/(?P<agent>[\w|\W]+)/(?P<action>[\w|\W]+)/$', 'get', name = "mcollective-rest-server"),
  url(r'^mcollective/(?P<filters>[\w|\W]+)/(?P<agent>[\w|\W]+)/(?P<action>[\w|\W]+)/(?P<args>[\w|\W]+)/$', 'get', name = "mcollective-rest-server"),
  url(r'^mcollective/(.*)', 'get'),
)
