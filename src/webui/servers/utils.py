from webui.servers.models import Server
from webui import settings, core
from guardian.shortcuts import get_objects_for_user
from webui.puppetclasses.models import PuppetClass
import logging
from webui.abstracts import ServerOperation

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


def get_server_operations(request, hostname):
    my_server = Server.objects.get(hostname=hostname)
    operations = {}  
    server_operations = core.kermit_modules.extract(ServerOperation)
    if server_operations:
        for op in server_operations:
            if op.get_visible(my_server, request.user):
                group_name = 'nogroup'
                group_icon = None
                if op.get_group_name():
                    group_name = op.get_group_name()
                    group_icon = op.get_group_icon()
                data = {"img": op.get_image(),
                        "name": op.get_name(),
                        "url": op.get_url(hostname),
                        "ismco": op.is_mcollective(), 
                        "hasparameters": op.request_parameters(),
                        "agent": op.get_agent(),
                        "action": op.get_action(),
                        "filter": op.get_filter(hostname),
                        "enabled": op.get_enabled(my_server),
                        "groupname": group_name,
                        "groupicon": group_icon}
                
                if not group_name in operations:
                    operations[group_name] = []
                operations[group_name].append(data)
            else:
                logger.debug("Operation %s is not visible for %s server" % (op.get_name(), hostname))
                
    return operations