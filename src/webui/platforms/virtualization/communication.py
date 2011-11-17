import logging
from webui.serverstatus.models import Server

logger = logging.getLogger(__name__)

def read_server_info(hostname):
    #Check if server accept virtualization
    #Means: libvirt module is installed
    server = Server.objects.get(hostname=hostname)
    libvirt_agent = server.agents.filter(name="libvirt")
    return len(libvirt_agent)>0
        