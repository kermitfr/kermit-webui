from django.conf.urls.defaults import *


urlpatterns = patterns('webui.progress.views',
    url(r'^get/(?P<taskname>[\w|\W]+)/(?P<taskid>[\w|\W]+)/$', 'get_progress', name = "get_progress"),)