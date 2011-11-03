from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    (r'^oc4j/', include('webui.platforms.oc4j.urls')),
    (r'^weblogic/', include('webui.platforms.weblogic.urls')),
    (r'^bar/', include('webui.platforms.bar.urls')),
    
    url(r'^application/(?P<appname>[\w|\W]+)/$', 'webui.platforms.views.appdetails', name = "application_details"),
)