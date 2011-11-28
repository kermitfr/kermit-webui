'''
Created on Aug 19, 2011

@author: mmornati
'''
from django.utils import simplejson as json
import logging
from celery.execute import send_task
from webui.platforms.platforms import platforms
from webui.platforms.abstracts import UpdatePlatform
from webui.widgets.loading import registry
from webui import settings

logger = logging.getLogger(__name__)

class Actions(object):

    def refresh_dashboard(self, user):
        logger.info("Getting all Widgets from database")
        try: 
            registry.reset_cache()
            widgets_list = registry.refresh_widgets()
            for widget in widgets_list:
                retrieved = registry.get_widget(widget['name'])
                retrieved.db_reference = widget

            json_data = json.dumps({'UUID': None, 'taskname': None})
            return json_data
        except Exception, err:
            logger.error('ERROR: ' + str(err))
                
    def refresh_server_basic_info(self, user):
        logger.info("Calling Refresh Basic Info")
        try: 
            result = send_task("webui.serverstatus.tasks.server_basic_info", [user])    
            json_data = json.dumps({'UUID': result.task_id, 'taskname':"webui.serverstatus.tasks.server_basic_info"})
            return json_data
        except Exception, err:
            logger.error('ERROR: ' + str(err))
        
    def refresh_server_inventory(self, user):
        logger.info("Calling Refresh Inventory")
        try: 
            updates_defined = platforms.extract(UpdatePlatform)
            result = send_task("webui.serverstatus.tasks.server_inventory", [user, updates_defined])    
            json_data = json.dumps({'UUID': result.task_id, 'taskname':"webui.serverstatus.tasks.server_inventory"})
            return json_data
        except Exception, err:
            logger.error('ERROR: ' + str(err))
    
    def update_agents(self, user):
        logger.info("Calling Update Agents Info")
        try: 
            result = send_task("webui.agent.tasks.updateagents", [user])    
            json_data = json.dumps({'UUID': result.task_id, 'taskname':"webui.agent.tasks.updateagents"})
            return json_data
        except Exception, err:
            logger.error('ERROR: ' + str(err))
      
    def update_user_groups(self, user):
        logger.info("Calling Refresh User Group")
        if 'a7x_wsgroups' in settings.INSTALLED_APPS:
            try: 
                result = send_task("a7x_wsgroups.tasks.update_groups", [])    
                json_data = json.dumps({'UUID': result.task_id, 'taskname':"a7x_wsgroups.tasks.update_groups"})
                return json_data
            except Exception, err:
                logger.error('ERROR: ' + str(err))
        else:
            logger.warn('Application Groups not installed')
            return json.dumps({'error':"Application Groups not installed"})
             
    
