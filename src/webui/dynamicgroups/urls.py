'''
Created on Jul 20, 2012

@author: mmornati
'''

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webui.dynamicgroups.views',
  url(r'^get_dynagroup_tree/$', 'get_dynamicgroup_tree', name = "get_dynamicgroup_tree"),
)
