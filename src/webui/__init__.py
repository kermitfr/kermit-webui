import logging
import copy
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
from webui import settings
import imp
import sys
from webui.core import kermit_modules

logger = logging.getLogger(__name__)

MODULES_TO_IMPORT = ["services", "operations"]

def initialize():
    logger.info("Initializing Kermit WebUI environment")
    """
    Auto-discover INSTALLED_APPS with MODULES_TO_IMPORT modules.
    """

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        if hasattr(mod, 'initialize'):
            try:
                mod.initialize()
            except:
                logger.error("ERROR initializing module %s! %s" % (app, sys.exc_info))
        else:
            logger.debug("App %s does not have initialization method" % app)
        
        for current_module in MODULES_TO_IMPORT:
            try:
                before_import_registry = copy.copy(kermit_modules._registry)
                import_module('%s.%s' % (app, current_module))
            except:
                kermit_modules._registry = before_import_registry
                if module_has_submodule(mod, current_module):
                    logger.error("Module %s found but there is an error importing it")
                    logger.error(sys.exc_info())
                    continue
