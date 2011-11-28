'''
Created on Nov 27, 2011

@author: mmornati
'''
from webui.serverstatus.models import Server
import logging

logger = logging.getLogger(__name__)

def construct_filters(servers):
    filters = None
    filter_servers = servers.split(';')
    for fs in filter_servers:
        server_db = Server.objects.get(fqdn=fs)
        if filters:
            filters = "%s_OR_%s" % (filters, server_db.hostname)
        else:
            filters = "identity_filter=%s" % server_db.hostname
        logger.debug("Filter generated: %s" % filters)
    return filters
    