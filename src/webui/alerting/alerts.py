'''
Created on Nov 7, 2011

@author: mmornati
'''
import logging
from webui.alerting.base import alertScheduler
from webui.alerting.abstracts import AlertJob
from webui.alerting.utils import send_server_inventory_email


logger = logging.getLogger(__name__)


class ServerListMailAlert(AlertJob):
    
    run_frequency = 86400
        
    def execute(self):
        logger.info("Sending report server email")
        send_server_inventory_email()
    
    
alertScheduler.register(ServerListMailAlert)