from django.conf.urls.defaults import *


urlpatterns = patterns('webui.upload.views',
    url(r'^getform/(?P<funcToCall>[\w|\W]+)/$', 'get_upload_form', name='get_upload_form'),
    url(r'^upload$', 'upload', name='upload'),
)