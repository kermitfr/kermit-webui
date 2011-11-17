from webui.platforms.virtualization.communication import read_server_info
from django.core.urlresolvers import reverse

import logging
from webui.platforms.abstracts import ServerTree
from webui.platforms.platforms import platforms
from webui.platforms.virtualization import settings

logger = logging.getLogger(__name__)


class VirtualizationServerTree(ServerTree):
    
    def getDetailsTree(self, hostname):
        server_info = read_server_info(hostname)
        content = {}
        #Configuring Instances
        if server_info:
            content = {"isFolder": False, "title": 'Virtualization', "key":'Virtualization', "icon":"virtualization.png", "detailsEnabled":"true", 'url': reverse('virtualization_details', kwargs={'hostname':hostname, 'instance_name':hostname, 'resource_name':hostname})}
        return content
    
    
platforms.register(VirtualizationServerTree, settings.PLATFORM_NAME)