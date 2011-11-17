'''
Created on Nov 17, 2011

@author: mmornati
'''
from django.conf.urls.defaults import *


urlpatterns = patterns('webui.alerting.views',
    url(r'^send_inventory_mail/$', 'send_inventory_mail', name='send_inventory_mail'),
)