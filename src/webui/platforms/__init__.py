import logging
import copy
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
import imp
from webui.platforms.platforms import platforms
import sys
import os
from webui.platforms import utils

logger = logging.getLogger(__name__)

BASE_PLATFORM_PATH = "webui.platforms"
MODULES_TO_IMPORT = ["tree", "updates", "applications", "operations"]

def initialize():
    logger.info("Initializing Platform environment")
    """
    Auto-discover INSTALLED_PLATFORMS with MODULES_TO_IMPORT modules.
    """

    installed_platforms = utils.installed_platforms_list()
    logger.info("Installed Platforms: %s" % installed_platforms)
    for platform in installed_platforms:
        mod = import_module("%s.%s" % (BASE_PLATFORM_PATH, platform))
        for current_module in MODULES_TO_IMPORT:
            try:
                before_import_registry = copy.copy(platforms._registry)
                import_module('%s.%s.%s' % (BASE_PLATFORM_PATH, platform, current_module))
            except:
                platforms._registry = before_import_registry
                if module_has_submodule(mod, current_module):
                    logger.error("Module %s found but there is an error importing it")
                    logger.error(sys.exc_info())
                    continue
