from django.http import HttpResponse
from webui.puppetclasses.models import PuppetClass
from django.utils import simplejson as json
import logging
from webui.serverstatus.models import Server
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

class QueryMethods(object):
    
    def get_tree_nodes(self, level, path):
        logger.info("Calling get_tree_nodes for level: " + str(level))
        classes = PuppetClass.objects.filter(enabled=True, level=level+1)
        data = []
        if path:
            path = path.replace('_', '/')
        else:
            path = ''
        for puppetclass in classes:
            test_path=path+'/'+puppetclass.name
            server = Server.objects.filter(puppet_path__startswith=test_path)
            if len(server)>0:
                content = {"isFolder": "true", "isLazy": "true", "title": puppetclass.name, "level":puppetclass.level, "key":puppetclass.name}
                data.append(content)
            else:
                logger.info("Excluding class " + str(puppetclass) + " because there are no server inside")
        
        #We cannot use / inside rest url, so / was substituted by _
        #Here we revert this change to obtain a correct path
        logger.info("Looking for servers in path: " + path)
        servers = Server.objects.filter(puppet_path=path, deleted=False)
        for server in servers:
            serverdata = {"title":server.fqdn, "url": "/server/details/"+server.fqdn+"/", "key":server.fqdn}
            data.append(serverdata)
             
        return json.dumps(data)
 
@login_required()       
def query(request, operation, level, path=None):
    query_methods = QueryMethods()
    methodToCall = getattr(query_methods, operation)
    int_node_id = int(level)
    return HttpResponse(methodToCall(int_node_id, path))
