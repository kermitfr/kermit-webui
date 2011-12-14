'''
Created on Nov 4, 2011

@author: mmornati
'''
from webui.platforms.abstracts import UpdatePlatform
import logging
from webui.restserver.communication import callRestServer
from webui.platforms.platforms import platforms
from webui.platforms.oc4j import settings

logger = logging.getLogger(__name__)


class OC4JUpdate(UpdatePlatform):
    
    def inventoryUpdate(self, user, use_another_task=True):
        logger.debug("Calling OC4J Inventory")
        try: 
            response, content = callRestServer(user, 'no-filter', 'a7xoas', 'inventory', None, True, use_another_task)
        except Exception, err:
            logger.error('ERROR: ' + str(err))

platforms.register(OC4JUpdate, settings.PLATFORM_NAME)