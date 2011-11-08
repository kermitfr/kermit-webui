import logging
from webui.django_cron.base import Job, cronScheduler
import sys
from webui import settings
from django.utils.importlib import import_module

logger = logging.getLogger(__name__)

def initialize():
    logger.info("Initializing Alerting module")
    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        try:
            import_module('%s.%s' % (app, 'alerts'))
        except:
            logger.debug("App %s does not have and alerts module" % app)