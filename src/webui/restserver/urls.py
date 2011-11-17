'''
Created on Aug 10, 2011

@author: mmornati
'''

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webui.restserver.views',
  #Response without templating
  url(r'^mcollective/(?P<filters>[\w|\W]+)/(?P<agent>[\w|\W]+)/(?P<action>[\w|\W]+)/$', 'get', name = "call_mcollective"),
  url(r'^mcollective-args/(?P<filters>[\w|\W]+)/(?P<agent>[\w|\W]+)/(?P<action>[\w|\W]+)/(?P<args>[\w|\W]+)/$', 'get', name = "call_mcollective_with_arguments"),
  #Response with template
  url(r'^mcollective-template/(?P<template>[\w|\W]+)/(?P<filters>[\w|\W]+)/(?P<agent>[\w|\W]+)/(?P<action>[\w|\W]+)/$', 'getWithTemplate', name = "call_mcollective_template"),
  url(r'^mcollective-template/(?P<template>[\w|\W]+)/(?P<filters>[\w|\W]+)/(?P<agent>[\w|\W]+)/(?P<action>[\w|\W]+)/(?P<args>[\w|\W]+)/$', 'getWithTemplate', name = "call_mcollective_template_with_arguments"),
  
  #Admin Actions
  url(r'^execute/(?P<action>[\w|\W]+)/(?P<type>[\w|\W]+)/$', 'executeAction', name = "action_executer"),
  
)
