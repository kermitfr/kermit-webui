'''
Created on Nov 7, 2012

@author: mmornati
'''
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('%s.views' % __package__,
  url(r'^createvm/(?P<hostname>[\w|\W]+)/$', 'create_vm', name = "ovirt_create_vm"),
)