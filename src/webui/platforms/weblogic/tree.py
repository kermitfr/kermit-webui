from webui.platforms.weblogic.communication import read_server_info
from django.core.urlresolvers import reverse
import logging
from webui.platforms.abstracts import ServerTree
from webui.platforms.platforms import platforms
from webui.platforms.weblogic import settings

logger = logging.getLogger(__name__)

class WebLogicServerTree(ServerTree):
    
    def getDetailsTree(self, hostname):
        server_info = read_server_info(hostname)
        content = {}
        #Configuring Instances
        if server_info:
            content = {"isFolder": True, "expand":True, "title": 'WebLogic', "key":'WebLogic', "icon":"bea_system_logo.png"}
            children = []
            logger.debug('Configuring Console')
            db_console = server_info["console"]
            console = {'title':db_console['name'], "key":db_console['name'], "icon":"console.png", "type":"console", "instance":db_console['name'],"detailsEnabled":"true", 'url': reverse('weblogic_console_details', kwargs={'hostname':hostname, 'resource_name':db_console['name']})}
            children.append(console)
            content['children'] = children 
            
            logger.debug('Configuring Node Managers')
            db_nodemanagers = {'title': 'Node Managers', 'isFolder':True, "key":"nodemanagers", "icon":"node-manager.png", "type":"nodemanagers"}
            nodemanagers = []
            for nodemanager in server_info['nodemanagers']:
                db = {'title':nodemanager['name'], "key":nodemanager['name'], "icon":"manager.png", "type":"nodemanager", "instance":nodemanager['name'],"detailsEnabled":"true", 'url': reverse('weblogic_nodemanager_details', kwargs={'hostname':hostname, 'resource_name':nodemanager['name']})}
                nodemanagers.append(db)
            db_nodemanagers['children'] = nodemanagers
            children.append(db_nodemanagers)
            content['children'] = children 
            
            logger.debug('Configuring Instances')
            db_instances = {'title': 'Instances', 'isFolder':True, "expand":True, "key":"instance", "icon":"app_server.png", "type":"instances"}
            instances = []
            for instance in server_info['instances']:
                db = {'title':instance['name'], "key":instance['name'], 'isFolder':True, "icon":"web_instance.png", "type":"instance", "instance":instance['name'],"detailsEnabled":"true", 'url': reverse('weblogic_instance_details', kwargs={'hostname':hostname, 'resource_name':instance['name']})}
                instance_children = []
                #Configuring Applications
                logger.debug('Configuring Applications')
                applications = {'title': 'Applications', 'isFolder':True, "key":"applications", "icon":"folder_applications.png", "type":"applications"}
                apps = []
                for appli in server_info['applilist']:
                    if instance['name'] == appli['target']:
                        app = {'title':appli['name'], "key":appli['name'], "icon":"application.png", "type":"application", "instance":instance['name'], "detailsEnabled":"true", 'url': reverse('weblogic_application_details', kwargs={'hostname':hostname, 'resource_name':appli['name']})}
                        apps.append(app)
                applications['children'] = apps
                instance_children.append(applications)
                
                #configuring datasources
                logger.debug('Configuring Datasources')
                db_datasources = {'title': 'Datasources', 'isFolder':True, "key":"datasources", "icon":"folder_database.png", "type":"datasources"}
                datasources = []
                for datasource in server_info['datasources']:
                    if instance['name'] in datasource['target']:
                        ds = {'title':datasource['name'], "key":datasource['name'], "icon":"datasource.png", "type":"datasource", "instance":datasource['name'],"detailsEnabled":"true", 'url': reverse('weblogic_datasource_details', kwargs={'hostname':hostname, 'resource_name':datasource['name']})}
                        datasources.append(ds)
                db_datasources['children'] = datasources
                instance_children.append(db_datasources)
                
                db['children'] = instance_children
                instances.append(db)
            db_instances['children'] = instances
            children.append(db_instances)
            
            content['children'] = children 
        return content
    
platforms.register(WebLogicServerTree, settings.PLATFORM_NAME)