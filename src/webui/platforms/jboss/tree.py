from webui.platforms.jboss.communication import read_server_info
from django.core.urlresolvers import reverse

import logging
from webui.platforms.abstracts import ServerTree
from webui.platforms.platforms import platforms
from webui.platforms.jboss import settings

logger = logging.getLogger(__name__)


class JbossServerTree(ServerTree):
    
    def getDetailsTree(self, hostname):
        server_info = read_server_info(hostname)
        content = {}
        #Configuring Instances
        if server_info:
            content = {"isFolder": True, "title": 'JBoss', "key":'JBoss', "icon":"jboss_logo.png", "detailsEnabled":"true", 'url': reverse('jboss_details', kwargs={'hostname':hostname, 'instance_name':hostname, 'resource_name':hostname})}
            logger.debug('Configuring Instances')
            db_instances = {'title': 'Instances', 'isFolder':True, "key":"instance", "icon":"app_server.png", "type":"instances"}
            dbs = []
            for instance in server_info["instances"]:
                db = {'title':instance['name'], "key":instance['name'], "icon":"web_instance.png", "type":"instance", "instance":instance['name']}
                #Configuring Applications
                logger.debug('Configuring Applications')
                applications = {'title': 'Applications', 'isFolder':True, "key":instance['name']+"applications", "icon":"folder_applications.png", "type":"applications"}
                apps = []
                for appli in instance['applilist']:
                    app = {'title':appli["name"], "key":appli["name"], "icon":"application.png", "type":"application", "instance":instance['name'], "detailsEnabled":"true", 'url': reverse('jboss_application_details', kwargs={'hostname':hostname, 'instance_name':instance['name'], 'resource_name':appli["name"]})}
                    apps.append(app)
                applications['children'] = apps
                
                #Configuring Datasources
                logger.debug('Configuring Datasources')
                datasources = {'title': 'Datasources', 'isFolder':True, "key":instance['name']+"datasources", "icon":"folder_database.png", "type":"datasources", "instance":instance['name']}
                dss = []
                for datasource in instance['datasources']:
                    datasource = {'title':datasource["jndi_name"], "key":datasource["jndi_name"], "icon":"datasource.png", "type":"datasource", "instance":instance['name'], "detailsEnabled":"true", 'url': reverse('jboss_datasource_details', kwargs={'hostname':hostname, 'instance_name':instance['name'], 'resource_name':datasource["jndi_name"]})}
                    dss.append(datasource)
                datasources['children'] = dss
                
                db['children'] = [datasources, applications]
                dbs.append(db)
            db_instances['children'] = dbs
            
            children = []
            children.append(db_instances)
            content['children'] = children 
        return content
    
    
platforms.register(JbossServerTree, settings.PLATFORM_NAME)