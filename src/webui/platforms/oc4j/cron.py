'''
Created on Aug 25, 2011

@author: mmornati
'''

from webui.django_cron import cronScheduler, Job
import logging

logger = logging.getLogger(__name__)

class UpdateOc4jPlatforms(Job):
        """
        Cron Job that calls mcollective updating oc4j platforms
        """
        
        #run every n seconds
        run_every = 3600

        def job(self):
            logger.info("Running Job UpdateOc4jPlatforms")
            
                
                
cronScheduler.register(UpdateOc4jPlatforms)