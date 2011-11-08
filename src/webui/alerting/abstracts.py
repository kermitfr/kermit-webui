'''
Created on Nov 7, 2011

@author: mmornati
'''
import logging
from webui.exceptions import NotImplementedAbstract

logger = logging.getLogger(__name__)

class AlertJob(object):
    
    run_frequency = 86400
        
    def execute(self):
        raise NotImplementedAbstract