'''
Created on Aug 10, 2011

@author: mmornati
'''

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webui.agent.views',
  #Response without templating
  url(r'^action/(?P<operation>[\w|\W]+)/(?P<agent>[\w|\W]+)/(?P<action>[\w|\W]+)/(?P<filters>[\w|\W]+)/(?P<dialog_name>[\w|\W]+)/(?P<response_container>[\w|\W]+)/$', 'query', name = "get-dialog-form"),
  url(r'^action/(?P<operation>[\w|\W]+)/$', 'query', name = "get-tree"),
  url(r'^form/post/(?P<agent>[\w|\W]+)/(?P<action>[\w|\W]+)/(?P<filters>[\w|\W]+)/(?P<dialog_name>[\w|\W]+)/(?P<response_container>[\w|\W]+)/(?P<xhr>.*)$', 'execute_action_form', name = "actionform"),
)
