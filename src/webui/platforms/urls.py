from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('',
    (r'^oc4j/', include('webui.platforms.oc4j.urls')),
    (r'^weblogic/', include('webui.platforms.weblogic.urls')),
    (r'^bar/', include('webui.platforms.bar.urls')),
)