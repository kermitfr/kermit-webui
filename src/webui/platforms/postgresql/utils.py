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
        response, content = callRestServer(user, filters, "postgresql", "sql_list", None, False, False)
        if response.getStatus() == 200:
            if content:
                #Looking for "intersections"
                sql_list = None
                for server_response in content:
                    if server_response.getStatusCode()==0 and server_response.getData():
                        if not sql_list:
                            sql_list = server_response.getData()['sqllist']
                        else:
                            sql_list = list(set(sql_list).intersection(server_response.getData()['sqllist']))
                    else:
                        logger.warn("No sqllist received")
                return json.dumps({"errors":"", "sqllist":sql_list})
            else:
                return json.dumps({"errors":"Cannot retrieve sqls list"})
    except Exception, err:  
        logger.error('ERROR: ' + str(err))
        