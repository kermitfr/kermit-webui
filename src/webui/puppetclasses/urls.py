'''
Created on Aug 10, 2011

@author: mmornati
'''

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webui.puppetclasses.views',
  #Response without templating
  url(r'^tree/(?P<operation>[\w|\W]+)/(?P<level>-{0,1}\d)/$', 'query', name = "get-tree"),
  url(r'^tree/(?P<operation>[\w|\W]+)/(?P<level>-{0,1}\d)/(?P<path>[\w|\W]+)/$', 'query', name = "get-tree"),
)
