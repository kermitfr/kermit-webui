from webui.platforms.postgresql.communication import read_server_info
from django.core.urlresolvers import reverse

import logging
from webui.platforms.abstracts import ServerTree
from webui.platforms.platforms import platforms
from webui.platforms.postgresql import settings

logger = logging.getLogger(__name__)


class PosgreSQLServerTree(ServerTree):
    
    def getDetailsTree(self, hostname):
        server_info = read_server_info(hostname)
        content = {}
        #Configuring Instances
        if server_info:
            content = {"isFolder": True, "title": 'PostgreSQL', "key":'PostgreSQL', "icon":"postgresql.png", "detailsEnabled":"true", 'url': reverse('postgres_details', kwargs={'hostname':hostname, 'database_name':hostname, 'resource_name':hostname})}
            logger.debug('Configuring Databases')
            db_instances = {'title': 'Databases', 'isFolder':True, "key":"databases", "icon":"folder_database.png", "type":"databases"}
            dbs = []
            for database in server_info["databases"]:
                db = {'title':database['name'], "key":database['name'], "icon":"database.png", "type":"database", "instance":database['name'], "detailsEnabled":"true", 'url': reverse('postgres_db_details', kwargs={'hostname':hostname, 'database_name':database['name'], 'resource_name':database['name']})}
                #Configuring Applications
                logger.debug('Configuring Tables')
                tables = {'title': 'Tables', 'isFolder':True, "key":"tables", "icon":"folder_documents.png", "type":"tables"}
                tabs = []
                for table in database['tables']:
                    tab = {'title':table, "key":table, "icon":"datasource.png", "type":"table", "database":database['name']}
                    tabs.append(tab)
                tables['children'] = tabs
                
                db['children'] = [tables]
                dbs.append(db)
            db_instances['children'] = dbs
            
            users_tree = {'title': 'Users', 'isFolder':True, "key":"users", "icon":"users.png", "type":"users"}
            users = []
            for user in server_info["users"]:
                user_tree = {'title':user['username'], "key":user['username'], "icon":"user.png", "type":"user"}
                users.append(user_tree)
            users_tree['children'] = users
            
            children = []
            children.append(db_instances)
            children.append(users_tree)
            content['children'] = children 
        return content
    
    
platforms.register(PosgreSQLServerTree, settings.PLATFORM_NAME)