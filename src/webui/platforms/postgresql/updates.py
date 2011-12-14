'''
Created on Nov 4, 2011

@author: mmornati
'''
from webui.platforms.abstracts import UpdatePlatform
import logging
from webui.restserver.communication import callRestServer
from webui.platforms.platforms import platforms
from webui.platforms.postgresql import settings

logger = logging.getLogger(__name__)


class PostgreSQLUpdate(UpdatePlatform):
    
    def inventoryUpdate(self, user, use_another_task=True):
        logger.debug("Calling PostgreSQL Inventory")
        try: 
            response, content = callRestServer(user, 'no-filter', 'postgresql', 'inventory', None, True, use_another_task)
        except Exception, err:
            logger.error('ERROR: ' + str(err))

platforms.register(PostgreSQLUpdate, settings.PLATFORM_NAME)