'''
Created on Nov 4, 2011

@author: mmornati
'''
from webui.platforms.abstracts import UpdatePlatform
import logging
from webui.restserver.communication import callRestServer
from webui.platforms.platforms import platforms
from webui.platforms.weblogic import settings

logger = logging.getLogger(__name__)


class WebLogicUpdate(UpdatePlatform):
    
    def inventoryUpdate(self, user, use_another_task=True):
        logger.debug("Calling WebLoginc Inventory")
        try: 
            response, content = callRestServer(user, 'no-filter', 'a7xows', 'inventory', None, True, use_another_task)
        except Exception, err:
            logger.error('ERROR: ' + str(err))

platforms.register(WebLogicUpdate, settings.PLATFORM_NAME)