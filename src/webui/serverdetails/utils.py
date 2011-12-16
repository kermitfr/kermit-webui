from webui.serverstatus.models import Server
from webui import settings
from guardian.shortcuts import get_objects_for_user
from webui.puppetclasses.models import PuppetClass
import logging

logger = logging.getLogger(__name__)

def extract_user_servers(user):
    if user.is_superuser:
        servers = Server.objects.all()
    else:
        if settings.FILTERS_SERVER:
            servers = get_objects_for_user(user, "use_server", Server).filter(deleted=False)
        elif settings.FILTERS_CLASS:
            servers = None
            for i in range (0, settings.LEVELS_NUMBER):
                level_classes = get_objects_for_user(user, "access_puppet_class", PuppetClass).filter(enabled=True, level=i)
                servers_list = Server.objects.filter(puppet_classes__in=level_classes, deleted=False).distinct()
                if servers:
                    servers = list(set(servers).intersection(set(servers_list)))
                else:
                    servers = servers_list
        else:
            servers = Server.objects.all()
            
    return servers


def extract_user_servers_in_path(user, server_path, start_with=True):
    logger.info("Looking for servers in path: " + server_path)
        
    if settings.FILTERS_SERVER:
        if start_with:
            servers = get_objects_for_user(user, "use_server", Server).filter(puppet_path__startswith=server_path, deleted=False)
        else:
            servers = get_objects_for_user(user, "use_server", Server).filter(puppet_path=server_path, deleted=False)
    else:
        if start_with:
            servers = Server.objects.filter(puppet_path__startswith=server_path, deleted=False)
        else:
            servers = Server.objects.filter(puppet_path=server_path, deleted=False)

    return servers