'''
Created on Aug 16, 2011

@author: mmornati
'''

from webui.django_cron import cronScheduler, Job
from webui.agent.utils import update_agents_info
import logging

logger = logging.getLogger(__name__)

class UpdateAgentsInfo(Job):
        """
        Cron Job that calls mcollective updating agent information
        """
        
        #run every n seconds
        #86400 = 1 time a day
        run_every = 86400

        def job(self):
            logger.info("Running Job UpdateAgentsInfo")
            update_agents_info()
                
                
cronScheduler.register(UpdateAgentsInfo)

