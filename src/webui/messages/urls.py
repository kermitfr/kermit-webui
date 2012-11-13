from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('webui.messages.views',
    url(r'^delete/(?P<message_id>[\w|\W]+)/$', 'delete_message', name = "delete_message"),
    url(r'^ignore/(?P<message_id>[\w|\W]+)/$', 'ignore_message', name = "ignore_message"),
)