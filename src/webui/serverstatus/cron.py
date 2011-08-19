'''
Created on Aug 16, 2011

@author: mmornati
'''

from webui.django_cron import cronScheduler, Job
import logging
from webui.restserver.utils import Operations

logger = logging.getLogger(__name__)

class UpdateServerStatus(Job):
        """
        Cron Job that calls mcollective updating server status in app db
        """
        
        #run every n seconds
        run_every = 3600

        def job(self):
            logger.info("Running Job UpdateServerStatus")
            ops = Operations()
            ops.server_basic_info()
                
                
cronScheduler.register(UpdateServerStatus)

