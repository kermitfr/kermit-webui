'''
Created on Sep 9, 2011

@author: mmornati
'''
from webui.restserver.communication import callRestServer
from django.utils import simplejson as json
import logging

logger = logging.getLogger(__name__)

def get_sql_list(user, filters):
    file_type = "sql"
    logger.debug("Calling get_sql_list with filters %s and type %s" % (filters, str(file_type)))
    try: 
        response, content = callRestServer(user, filters, "a7xdeploy", "applist", "apptype="+str(file_type))
        if response.status == 200:
            jsonObj = json.loads(content)
            if jsonObj:
                #Looking for "intersections"
                sql_list = None
                for server_response in jsonObj:
                    if not sql_list:
                        sql_list = server_response['data']['applist']
                    else:
                        sql_list = set(sql_list).intersection(server_response['data']['applist'])
                return json.dumps({"errors":"", "sqllist":sql_list})
            else:
                return json.dumps({"errors":"Cannot retrieve sqls list"})
    except Exception, err:  
        logger.error('ERROR: ' + str(err))