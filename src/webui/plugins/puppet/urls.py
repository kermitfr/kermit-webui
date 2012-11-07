'''
Created on Nov 7, 2012

@author: mmornati
'''
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('%s.views' % __package__,
  url(r'^edit/(?P<hostname>[\w|\W]+)/$', 'server_edit', name = "editserver"),
  url(r'^submit/(?P<hostname>[\w|\W]+)/$', 'submit_server_edit', name = "submit_server_edit"),
)