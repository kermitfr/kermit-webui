'''
Created on Nov 4, 2011

@author: mmornati
'''
from webui.platforms.abstracts import UpdatePlatform
import logging
from webui.restserver.communication import callRestServer
from webui.platforms.platforms import platforms
from webui.platforms.bar import settings

logger = logging.getLogger(__name__)


class BarUpdate(UpdatePlatform):
    
    def inventoryUpdate(self, user, use_another_task=True):
        logger.debug("Calling BAR Inventory")
        try: 
            response, content = callRestServer(user, 'no-filter', 'a7xbar', 'inventory', None, True, use_another_task)
        except Exception, err:
            logger.error('ERROR: ' + str(err))

platforms.register(BarUpdate, settings.PLATFORM_NAME)