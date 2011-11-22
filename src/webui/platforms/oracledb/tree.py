from webui.platforms.oracledb.communication import read_server_info
from django.core.urlresolvers import reverse

import logging
from webui.platforms.abstracts import ServerTree
from webui.platforms.platforms import platforms
from webui.platforms.oracledb import settings

logger = logging.getLogger(__name__)


class OracleDBServerTree(ServerTree):
    
    def getDetailsTree(self, hostname):
        server_info = read_server_info(hostname)
        content = {}
        #Configuring Instances
        if server_info:
            content = {"isFolder": True, "title": 'OracleDB', "key":'OracleDB', "icon":"oracle_db.png"}
            logger.debug('Configuring Databases')
            db_instances = {'title': 'Databases', 'isFolder':True, "key":"databases", "icon":"folder_database.png", "type":"databases"}
            dbs = []
            for instance in server_info["instances"]:
                db = {'title':instance['instance_name'], "key":instance['instance_name'], "icon":"database.png", "type":"database", "instance":instance['instance_name'], "detailsEnabled":"true", 'url': reverse('oracledb_instance_details', kwargs={'hostname':hostname, 'database_name':instance['instance_name'], 'resource_name':instance['instance_name']})}
                #Configuring Applications
#                logger.debug('Configuring Tables')
#                tables = {'title': 'Tables', 'isFolder':True, "key":"tables", "icon":"folder_documents.png", "type":"tables"}
#                tabs = []
#                for table in database['tables']:
#                    tab = {'title':table, "key":table, "icon":"datasource.png", "type":"table", "database":database['name']}
#                    tabs.append(tab)
#                tables['children'] = tabs
                
#                db['children'] = [tables]
                dbs.append(db)
            db_instances['children'] = dbs
            
            children = []
            children.append(db_instances)
            content['children'] = children 
        return content
    
    
platforms.register(OracleDBServerTree, settings.PLATFORM_NAME)