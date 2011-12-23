from django.http import HttpResponse
from webui.puppetclasses.models import PuppetClass
from django.utils import simplejson as json
import logging
from webui.serverstatus.models import Server
from django.contrib.auth.decorators import login_required
from guardian.shortcuts import get_objects_for_user
from webui import settings
from webui.core import kermit_modules
from webui.abstracts import ContextOperation

logger = logging.getLogger(__name__)

class QueryMethods(object):
        
    def get_tree_nodes(self, user, level, path):
        logger.info("Calling get_tree_nodes for level: " + str(level))
        if settings.FILTERS_CLASS:
            classes = get_objects_for_user(user, 'access_puppet_class', PuppetClass).filter(enabled=True, level=level+1)
        else:
            classes = PuppetClass.objects.filter(enabled=True, level=level+1)
        data = []
        #We cannot use the character / inside rest url, so '/' was substituted by '_'
        #Here we revert this change to obtain the correct path
        if path:
            path = path.replace('_', '/')
        else:
            path = ''
        for puppetclass in classes:
            test_path=path+'/'+puppetclass.name
            servers = Server.objects.filter(puppet_path__startswith=test_path)
            if not user.is_superuser and settings.FILTERS_SERVER:
                servers = get_objects_for_user(user, 'use_server', Server).filter(puppet_path__startswith=test_path)
#            elif not user.is_superuser and level==0:
#                logger.debug("Hide servers with no class for non-admin users")
#                servers = []
                
            if len(servers)>0:
                classes = check_context_operation_visibility_list(servers)
                content = {"isFolder": "true", "isLazy": "false", "title": puppetclass.name, "level":puppetclass.level, "key":puppetclass.name, "filtername":puppetclass.name, "classes": classes}
                data.append(content)
            else:
                logger.info("Excluding class " + str(puppetclass) + " because there are no server inside")
        
        logger.info("Looking for servers in path: " + path)
        servers = Server.objects.filter(puppet_path=path, deleted=False)
        if not user.is_superuser and settings.FILTERS_SERVER:
            servers = get_objects_for_user(user, 'use_server', Server).filter(puppet_path=path, deleted=False)
        for server in servers:
            classes = check_context_operation_visibility(server)
            serverdata = {"title":server.fqdn, "url": settings.BASE_URL + "/server/details/"+server.hostname+"/", "key":server.fqdn, "filtername":server.hostname, "classes": classes}
            data.append(serverdata)
             
        return json.dumps(data)
    
def check_context_operation_visibility_list(servers):
    classes = []
    for server in servers:
        classes.extend(check_context_operation_visibility(server))
    return classes
    
def check_context_operation_visibility(server): 
    context_operations = kermit_modules.extract(ContextOperation)
    classes = []
    if context_operations:
        for c_op in context_operations:
            if c_op.get_visible(server):
                current_class = c_op.get_type()
                if current_class and not current_class in classes:
                    classes.append(current_class)
    return classes
                
 
@login_required()       
def query(request, operation, level, path=None):
    query_methods = QueryMethods()
    methodToCall = getattr(query_methods, operation)
    int_node_id = int(level)
    return HttpResponse(methodToCall(request.user, int_node_id, path))
