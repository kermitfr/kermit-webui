from django.conf.urls.defaults import patterns, include, url
from webui.platforms import utils
import logging
import imp
import os

logger = logging.getLogger(__name__)

urlpatterns = patterns('',
    url(r'^application/(?P<appname>[\w|\W]+)/$', 'webui.platforms.views.appdetails', name = "application_details"),
)

installed_platforms = utils.installed_platforms_list()

for platform in installed_platforms:
    try:
        urlpatterns += patterns('',
             (r"^%s/" % platform, include("webui.platforms.%s.urls" % platform)),
        )
    except:
        logger.debug ("Platform %s does not provides urls" % platform)