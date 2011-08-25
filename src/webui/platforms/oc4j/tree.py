from webui.platforms.oc4j.communication import read_server_info

import logging
from django.http import HttpResponse

logger = logging.getLogger(__name__)

def getDetailsTree(hostname):
    server_info = read_server_info(hostname)
    content = {}
    base_url = '/platform/oc4j/details/'
    #Configuring Instances
    if server_info:
        content = {"isFolder": "true", "title": 'OC4J', "key":'OC4J', "icon":"server.png"}
        logger.debug('Configuring Instances')
        db_instances = {'title': 'Instances', 'isFolder':"true", "key":"instance", "icon":"app_server.png", "type":"instances"}
        dbs = []
        for instance in server_info:
            db = {'title':instance['id'], "key":instance['id'], "icon":"web_instance.png", "type":"instance", "instance":instance['id'],"detailsEnabled":"true", 'url': base_url + hostname + '/' + instance['id'] + '/' + instance['id'] + '/instance/'}
            #Configuring Applications
            logger.debug('Configuring Applications')
            applications = {'title': 'Applications', 'isFolder':"true", "key":"applications", "icon":"folder_applications.png", "type":"applications"}
            apps = []
            for appli in instance['applilist']:
                app = {'title':appli['name'], "key":appli['name'], "icon":"application.png", "type":"application", "instance":instance['id'], "detailsEnabled":"true", 'url': base_url + hostname + '/' + instance['id'] + '/' + appli['name'] + '/application/'}
                apps.append(app)
            applications['children'] = apps
            
            #Configuring Datasources
            logger.debug('Configuring Datasources')
            datasources = {'title': 'Datasources', 'isFolder':"true", "key":"datasources", "icon":"folder_database.png", "type":"datasources", "instance":instance['id'], "detailsEnabled":"true", 'url': base_url + hostname + '/' + instance['id'] + '/' + instance['id'] + '/datasources/'}
            dss = []
            for datasource in instance['datasource']:
                datasource_url = datasource['name'].replace('/', '_')
                datasource = {'title':datasource['name'], "key":datasource['name'], "icon":"datasource.png", "type":"datasource", "instance":instance['id'], "detailsEnabled":"true", 'url': base_url + hostname + '/' + instance['id'] + '/' + datasource_url + '/datasource/'}
                dss.append(datasource)
            datasources['children'] = dss
            
            db['children'] = [datasources, applications]
            dbs.append(db)
        db_instances['children'] = dbs
        
        children = []
        children.append(db_instances)
        content['children'] = children 
    return content