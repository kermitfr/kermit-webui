'''
Created on Sep 9, 2011

@author: mmornati
'''
from webui.restserver.communication import callRestServer
from django.utils import simplejson as json
import logging

logger = logging.getLogger(__name__)

def get_apps_list(filters, file_type):
    logger.debug("Calling app_list with filters %s and type %s" % (filters, str(file_type)))
    try: 
        response, content = callRestServer(filters, "a7xdeploy", "applist", "apptype="+str(file_type))
        if response.status == 200:
            jsonObj = json.loads(content)
            if jsonObj:
                #Looking for "intersections"
                app_list = None
                for server_response in jsonObj:
                    if not app_list:
                        app_list = server_response['data']['applist']
                    else:
                        app_list = set(app_list).intersection(server_response['data']['applist'])
                return json.dumps({"errors":"", "applist":app_list})
            else:
                return json.dumps({"errors":"Cannot retrieve apps list"})
    except Exception, err:  
        logger.error('ERROR: ' + str(err))