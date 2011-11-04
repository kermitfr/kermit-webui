from webui.platforms.oc4j.communication import read_server_info
from django.core.urlresolvers import reverse

import logging
from webui.platforms.abstracts import ServerTree
from webui.platforms.oc4j import settings
from webui.platforms.platforms import platforms

logger = logging.getLogger(__name__)

class OC4JServerTree(ServerTree):
    
    def getDetailsTree(self, hostname):
        server_info = read_server_info(hostname)
        content = {}
        #Configuring Instances
        if server_info:
            content = {"isFolder": True, "expand": True, "title": 'OC4J', "key":'OC4J', "icon":"oracle_logo.png"}
            logger.debug('Configuring Instances')
            db_instances = {'title': 'Instances', 'isFolder':True, "expand":True, "key":"instance", "icon":"app_server.png", "type":"instances"}
            dbs = []
            for instance in server_info:
                db = {'title':instance['id'], "key":instance['id'], "icon":"web_instance.png", "type":"instance", "instance":instance['id'],"detailsEnabled":"true", 'url': reverse('oc4j_instance_details', kwargs={'hostname':hostname, 'instance_name':instance['id'], 'resource_name':instance['id']})}
                #Configuring Applications
                logger.debug('Configuring Applications')
                applications = {'title': 'Applications', 'isFolder':True, "key":"applications", "icon":"folder_applications.png", "type":"applications"}
                apps = []
                for appli in instance['applilist']:
                    app = {'title':appli['name'], "key":appli['name'], "icon":"application.png", "type":"application", "instance":instance['id'], "detailsEnabled":"true", 'url': reverse('oc4j_application_details', kwargs={'hostname':hostname, 'instance_name':instance['id'], 'resource_name':appli['name']})}
                    apps.append(app)
                applications['children'] = apps
                
                #Configuring Datasources
                logger.debug('Configuring Datasources')
                datasources = {'title': 'Datasources', 'isFolder':True, "key":"datasources", "icon":"folder_database.png", "type":"datasources", "instance":instance['id'], "detailsEnabled":"true", 'url': reverse('oc4j_datasources_details', kwargs={'hostname':hostname, 'instance_name':instance['id'], 'resource_name':instance['id']})}
                dss = []
                for datasource in instance['datasource']:
                    datasource_url = datasource['name'].replace('/', '_')
                    datasource = {'title':datasource['name'], "key":datasource['name'], "icon":"datasource.png", "type":"datasource", "instance":instance['id'], "detailsEnabled":"true", 'url': reverse('oc4j_datasource_details', kwargs={'hostname':hostname, 'instance_name':instance['id'], 'resource_name':datasource_url})}
                    dss.append(datasource)
                datasources['children'] = dss
                
                db['children'] = [datasources, applications]
                dbs.append(db)
            db_instances['children'] = dbs
            
            children = []
            children.append(db_instances)
            content['children'] = children 
        return content
    
platforms.register(OC4JServerTree, settings.PLATFORM_NAME)