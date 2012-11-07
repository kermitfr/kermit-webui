'''
Created on Nov 7, 2012

@author: mmornati
'''
from django.conf.urls.defaults import patterns, include
import logging
from webui.plugins import utils

logger = logging.getLogger(__name__)

urlpatterns = patterns('',
)

installed_plugins = utils.installed_plugins_list()


for plugin in installed_plugins:
    try:
        urlpatterns += patterns('',
             (r"^%s/" % plugin, include("webui.plugins.%s.urls" % plugin)),
        )
    except:
        logger.debug ("Plugin %s does not provides urls" % plugin)