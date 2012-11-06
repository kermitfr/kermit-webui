from django.conf.urls.defaults import patterns, include, url
from webui.platforms import utils

urlpatterns = patterns('',
    url(r'^application/(?P<appname>[\w|\W]+)/$', 'webui.platforms.views.appdetails', name = "application_details"),
)

installed_platforms = utils.installed_platforms_list()

for platform in installed_platforms:
    urlpatterns += patterns('',
         (r"^%s/" % platform, include("webui.platforms.%s.urls" % platform)),
    )