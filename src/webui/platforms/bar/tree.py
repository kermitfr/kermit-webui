from webui.platforms.bar.communication import read_server_info
from django.core.urlresolvers import reverse

import logging
from webui.platforms.abstracts import ServerTree
from webui.platforms.bar import settings
from webui.platforms.platforms import platforms

logger = logging.getLogger(__name__)

class BarServerTree(ServerTree):
    
    def getDetailsTree(self, hostname):
        server_info = read_server_info(hostname)
        content = {}
        #Configuring Instances
        if server_info:
            content = {"isFolder": True, "expand":True, "title": 'Consoles', "key":'consoles', "icon":"console_bar.png"}
            logger.debug('Configuring Bar')
            consoles = []
            for console in server_info:
                #Configure Console
                console_dict = {"isFolder": True, "title": console['consolename'], "key":console['consolename'], "icon":"console_bar.png", "detailsEnabled": "true", 'url': reverse('bar_console_details', kwargs={'hostname':hostname, 'console_name':console['consolename'], 'resource_name':console['consolename']})}
                #Configure Batch Archives
                batch = {'title': 'Batch', 'isFolder':True, "key":"batchlist", "icon":"batch_process.png", "type":"batch", "console":console["consolename"]}
                bars = []
                for bar in console['barlist']:
                    bar_dict = {'title':bar['name'], "key":bar['name'], "icon":"console.png", "type":"bar", "detailsEnabled":"true", "url": reverse('bar_details', kwargs={'hostname':hostname, 'console_name':console['consolename'], 'resource_name':bar['name']})}
                    bars.append(bar_dict)
                batch['children'] = bars    
                
                #Configure PoolList
                pool_menu = {'title': 'Pools', 'isFolder':True, "key":"poollist", "icon":"folder_database.png", "type":"pool", "console":console["consolename"], "detailsEnabled":"true", "url": reverse('bar_pools_details', kwargs={'hostname':hostname, 'console_name':console['consolename'], 'resource_name':console['consolename']})}
                pools = []
                for pool in console['poollist']:
                    pool_url = pool['poolname'].replace('/', '_')
                    pool_dict = {'title':pool['poolname'], "key":pool['poolname'], "icon":"datasource.png", "type":"pool", "detailsEnabled":"true", "url": reverse('bar_pool_details', kwargs={'hostname':hostname, 'console_name':console['consolename'], 'resource_name':pool_url})}
                    pools.append(pool_dict)
                pool_menu['children'] = pools   
                
                console_dict['children'] = [batch, pool_menu]
                consoles.append(console_dict)
                  
                    
            content['children'] = consoles 
        return content
    
platforms.register(BarServerTree, settings.PLATFORM_NAME)
