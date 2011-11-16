'''
Created on Aug 16, 2011

@author: mmornati
'''
from celery.execute import send_task
from webui.django_cron import cronScheduler, Job
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
            result = send_task("webui.agent.tasks.updateagents", ['AgentInfoCron'])    
                
cronScheduler.register(UpdateAgentsInfo)

