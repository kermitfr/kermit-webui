'''
Created on Jul 20, 2012

@author: mmornati
'''

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webui.dynamicgroups.views',
  url(r'^get_tree/$', 'get_dynamicgroup_tree', name = "get_dynamicgroup_tree"),
  url(r'^get_form/$', 'get_dynamicgroup_form', name = "get_dynamicgroup_form_no_param"),
  url(r'^get_form/(?P<dynagroup_id>[\w|\W]+)/$', 'get_dynamicgroup_form', name = "get_dynamicgroup_form"),
  url(r'^del/(?P<dynagroup_id>[\w|\W]+)/$', 'delete_dynamicgroup', name = "delete_dynamicgroup"),
  url(r'^refresh/(?P<dynagroup_id>[\w|\W]+)/$', 'refresh_dynamicgroup', name = "refresh_dynamicgroup"),
  url(r'^post_form/(?P<xhr>.*)$', 'post_dynagroup_mods', name = "post_dynagroup_mods"),
)
