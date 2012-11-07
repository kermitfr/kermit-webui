import logging
import copy
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
import imp
import sys
import os
from webui.plugins import utils
from webui.widgets.loading import registry
from webui.plugins.plugins import plugins

logger = logging.getLogger(__name__)

BASE_PLUGIN_PATH = "webui.plugins"
MODULES_TO_IMPORT = ["tree", "updates", "applications", "operations"]
CHECK_WIDGETS = True

def initialize():
    logger.info("Initializing Plugins environment")
    """
    Auto-discover INSTALLED_MODULES with MODULES_TO_IMPORT modules.
    """

    installed_plugins = utils.installed_plugins_list()
    logger.info("Installed Plugins: %s" % installed_plugins)
    for plugin in installed_plugins:
        mod = import_module("%s.%s" % (BASE_PLUGIN_PATH, plugin))
        for current_module in MODULES_TO_IMPORT:
            try:
                before_import_registry = copy.copy(plugins._registry)
                import_module('%s.%s.%s' % (BASE_PLUGIN_PATH, plugin, current_module))
            except:
                plugins._registry = before_import_registry
                if module_has_submodule(mod, current_module):
                    logger.error("Module %s found but there is an error importing it")
                    logger.error(sys.exc_info())
                    continue
                
        if CHECK_WIDGETS:
            try:
                imp.find_module("widgets", mod.__path__)
                registry.inject_widget("%s.%s" % (BASE_PLUGIN_PATH, plugin))
            except ImportError:
                logger.debug ("Plugin %s does not provides widgets" % plugin)
                
        