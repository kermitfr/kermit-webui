'''
Created on Aug 10, 2011

@author: mmornati
'''

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webui.puppetclasses.views',
  #Response without templating
  url(r'^tree/*', 'query', name = "mcollective-rest-server"),
)
