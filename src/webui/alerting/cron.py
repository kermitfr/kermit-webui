'''
Created on Aug 16, 2011

@author: mmornati
'''

from webui.django_cron import cronScheduler, Job
import logging
from webui.alerting.models import Alert
from datetime import datetime
import sys
from django.utils.importlib import import_module

logger = logging.getLogger(__name__)

class CheckAlerts(Job):
        """
        Cron Job that check if there's alert to fire
        """
        
        #run every n seconds
        run_every = 86400

        def job(self):

            logger.info("Running Job %s" % __name__)
            alerts = Alert.objects.all()
            for alert in alerts:
                if alert.enabled:
                    time_delta = datetime.now() - alert.last_run
                    if (time_delta.seconds + 86400*time_delta.days) > alert.run_frequency:
                        logger.debug("Sending Mail for %s" % alert.name)    
                        try:
                            mod = import_module(alert.module)
                            for method in vars(mod):
                                if method.endswith("Alert") and method != "Alert":
                                    klass = getattr(mod, method)
                                    instance = klass()
                                    break
                            if instance:
                                instance.execute()
                        except Exception:
                            logger.error("Error executing alert %s! %s" % (alert.name, sys.exc_info()))
                
                
cronScheduler.register(CheckAlerts)

