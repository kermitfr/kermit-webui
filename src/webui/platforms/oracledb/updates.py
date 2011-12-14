'''
Created on Nov 4, 2011

@author: mmornati
'''
from webui.platforms.abstracts import UpdatePlatform
import logging
from webui.restserver.communication import callRestServer
from webui.platforms.platforms import platforms
from webui.platforms.oracledb import settings

logger = logging.getLogger(__name__)


class OracleDBUpdate(UpdatePlatform):
    
    def inventoryUpdate(self, user, use_another_task=True):
        logger.debug("Calling OracleDB Inventory")
        try: 
            response, content = callRestServer(user, 'no-filter', 'oracledb', 'inventory', None, True, use_another_task)
        except Exception, err:
            logger.error('ERROR: ' + str(err))

platforms.register(OracleDBUpdate, settings.PLATFORM_NAME)