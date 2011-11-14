'''
Created on Nov 14, 2011

@author: mmornati
'''
import logging
from webui.restserver.communication import callRestServer
from django.utils import simplejson as json

logger = logging.getLogger(__name__)

def sql_list(user, filters):
    file_type = "sql"
    logger.debug("Calling get_sql_list with filters %s and type %s" % (filters, str(file_type)))
    try: 
        response, content = callRestServer(user, filters, "postgresql", "sql_list")
        if response.status == 200:
            jsonObj = json.loads(content)
            if jsonObj:
                #Looking for "intersections"
                sql_list = None
                for server_response in jsonObj:
                    if not sql_list:
                        sql_list = server_response['data']['sqllist']
                    else:
                        sql_list = set(sql_list).intersection(server_response['data']['applist'])
                return json.dumps({"errors":"", "sqllist":sql_list})
            else:
                return json.dumps({"errors":"Cannot retrieve sqls list"})
    except Exception, err:  
        logger.error('ERROR: ' + str(err))
        