'''
Created on Aug 10, 2011

@author: mmornati
'''

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webui.saml.views',
  url(r'^SSO$', 'SSO', name = "saml_sso"),
  url(r'^logout/$', 'logout', name = "saml_logout"),
  url(r'^test/$', 'test', name = "saml_test"),
  
)
