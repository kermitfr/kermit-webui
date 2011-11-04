from webui.serverstatus.models import Server
from webui import settings
from guardian.shortcuts import get_objects_for_user
from webui.puppetclasses.models import PuppetClass


def extract_user_servers(user):
    if user.is_superuser:
        servers = Server.objects.all()
    else:
        if settings.FILTERS_SERVER:
            servers = get_objects_for_user(user, "use_server", Server).filter(deleted=False)
        elif settings.FILTERS_CLASS:
            puppet_classes = get_objects_for_user(user, "access_puppet_class", PuppetClass).filter(enabled=True)
            servers = Server.objects.filter(puppet_classes__in=puppet_classes, deleted=False).distinct()
        else:
            servers = Server.objects.all()
            
    return servers