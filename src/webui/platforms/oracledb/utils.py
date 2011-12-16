'''
Created on Nov 14, 2011

@author: mmornati
'''
import logging
from webui.restserver.communication import callRestServer
from django.utils import simplejson as json
from webui.platforms.oracledb.communication import read_server_info
from webui.serverstatus.models import Server

logger = logging.getLogger(__name__)

def sql_list(user, filters):
    file_type = "sql"
    logger.debug("Calling get_sql_list with filters %s and type %s" % (filters, str(file_type)))
    try: 
        #Does not use celery for fast operations (with celery it's longer)
        response, content = callRestServer(user, filters, "oracledb", "sql_list", None, False, False)
        if response.status == 200:
            jsonObj = json.loads(content)
            if jsonObj:
                #Looking for "intersections"
                sql_list = None
                for server_response in jsonObj:
                    if server_response['statuscode']==0 and server_response['data']:
                        if not sql_list:
                            sql_list = server_response['data']['sqllist']
                        else:
                            sql_list = list(set(sql_list).intersection(server_response['data']['sqllist']))
                    else:
                        logger.warn("No sqllist in server response")
                return json.dumps({"errors":"", "sqllist":sql_list})
            else:
                return json.dumps({"errors":"Cannot retrieve sqls list"})
    except Exception, err:  
        logger.error('ERROR: ' + str(err))
        
        
def extract_instances_name(hostname):
    instances = []
    server_info = read_server_info(hostname)
    if server_info:
        for instance in server_info['instances']:
            instances.append(instance['instance_name'])
        
    return instances

def extract_schema(hostname, instancename):
    schemas = []
    server_info = read_server_info(hostname)
    for instance in server_info['instances']:
        if instancename == instance['instance_name']:
            found_instance = instance
            break
    if found_instance:
        for schema in found_instance['data']:
            schemas.append(schema['user_name'])
    else:
        logger.info("Cannot find instance %s" % instancename)
    return schemas


def extract_compatible_servers(schema_name):
    servers = Server.objects.filter(deleted=False)
    compatible_servers = []
    for server in servers:
        server_info = read_server_info(server.hostname)
        if server_info:
            for instance in server_info['instances']:
                for data in instance['data']:
                    if data['user_name'] == schema_name:
                        compatible_servers.append({"server": server.hostname, "instance": instance['instance_name']})
                        break
    return compatible_servers
    
        