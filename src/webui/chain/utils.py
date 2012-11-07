'''
Created on Nov 27, 2011

@author: mmornati
'''
from webui.servers.models import Server
import logging

logger = logging.getLogger(__name__)

def construct_filters(servers, agent_name=None):
    filters = None
    filter_servers = servers.split(';')
    for fs in filter_servers:
        if agent_name:
            logger.debug("Checking for wrong server.")
            if check_server(fs, agent_name):
                logger.debug("Found a wrong server in the list. Excluding")
                continue
        server_db = Server.objects.get(fqdn=fs)
        if filters:
            if not server_db.hostname in filters:
                filters = "%s_OR_%s" % (filters, server_db.hostname)
        else:
            filters = "identity=%s" % server_db.hostname
    logger.debug("Filter generated: %s" % filters)
    return filters
    
def check_servers(servers, agent_name):
    servers_list = servers.split(';')
    for server in servers_list:
        server_name = check_server(server, agent_name)
        if server_name:
            return server_name
    return None

def check_server(server, agent_name):
    try:
        db_server = Server.objects.get(hostname=server)
    except:
        logger.info("No server with the given hostname. Checking fqdn")
        try:
            db_server = Server.objects.get(fqdn=server)
        except:
            logger.warn("No server found both with hostname and fqdn!")
            return None
    
    if db_server:
        agent = db_server.agents.filter(name=agent_name)
        if len(agent)==0:
            return server
    return None