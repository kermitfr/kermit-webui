from webui.platforms.jboss.communication import read_server_info
from django.core.urlresolvers import reverse

import logging

logger = logging.getLogger(__name__)

def getDetailsTree(hostname):
    server_info = read_server_info(hostname)
    content = {}
    #Configuring Instances
    if server_info:
        content = {"isFolder": True, "expand": True, "title": 'JBoss', "key":'JBoss', "icon":"jboss-logo.jpg", "detailsEnabled":"true", 'url': reverse('jboss_details', kwargs={'hostname':hostname, 'instance_name':hostname, 'resource_name':hostname})}
        logger.debug('Configuring Instances')
        db_instances = {'title': 'Instances', 'isFolder':True, "expand":True, "key":"instance", "icon":"app_server.png", "type":"instances"}
        dbs = []
        for instance in server_info["instances"]:
            db = {'title':instance['name'], "key":instance['name'], "icon":"web_instance.png", "type":"instance", "instance":instance['name']}
            #Configuring Applications
            logger.debug('Configuring Applications')
            applications = {'title': 'Applications', 'isFolder':True, "key":"applications", "icon":"folder_applications.png", "type":"applications"}
            apps = []
            for appli in instance['applilist']:
                app = {'title':appli, "key":appli, "icon":"application.png", "type":"application", "instance":instance['name']}
                apps.append(app)
            applications['children'] = apps
            
            #Configuring Datasources
            logger.debug('Configuring Datasources')
            datasources = {'title': 'Datasources', 'isFolder':True, "key":"datasources", "icon":"folder_database.png", "type":"datasources", "instance":instance['name']}
            dss = []
            for datasource in instance['datasources']:
                datasource = {'title':datasource, "key":datasource, "icon":"datasource.png", "type":"datasource", "instance":instance['name']}
                dss.append(datasource)
            datasources['children'] = dss
            
            db['children'] = [datasources, applications]
            dbs.append(db)
        db_instances['children'] = dbs
        
        children = []
        children.append(db_instances)
        content['children'] = children 
    return content