from django.http import HttpResponse
from webui.puppetclasses.models import PuppetClass
from django.utils import simplejson as json
import logging
from webui.serverstatus.models import Server

logger = logging.getLogger(__name__)

class QueryMethods(object):
    
    def get_tree_nodes(self, level, path):
        logger.info("Calling get_tree_nodes for level: " + str(level))
        #Call for parent
        classes = PuppetClass.objects.filter(enabled=True, level=level+1)
        data = []
        for puppetclass in classes:
            content = {"isFolder": "true", "isLazy": "true", "title": puppetclass.name, "level":puppetclass.level, "key":puppetclass.name}
            data.append(content)
        
        if path:
            #We cannot use / inside rest url, so / was substituted by _
            #Here we revert this change to obtain a correct path
            path = path.replace('_', '/')
            logger.info("Looking for servers in path: " + path)
            servers = Server.objects.filter(puppet_path=path)
            for server in servers:
                serverdata = {"title":server.hostname, "url": "/server/details/"+server.hostname+"/", "key":server.hostname}
                data.append(serverdata)
             
        return json.dumps(data)
    
    def get_child_data(self, current_node):
        childlist = []
        for child in current_node.children.all():
            #children = self.get_child_data(child)
            childata = {"isFolder":"true", "isLazy": "true", "title":child.name, "id":current_node.pk}
            childlist.append(childata) 
           
        if len(childlist) == 0:
            logger.info("Retrieving servers contained in class " + current_node.name)
            #Getting server in current class
            servers = Server.objects.filter(puppet_classes=current_node)
            for server in servers:
                childata = {"title":server.hostname, "url": "/server/details/"+server.hostname+"/"}
                childlist.append(childata) 
            
        return childlist
        
def query(request, operation, level, path=None):
    query_methods = QueryMethods()
    methodToCall = getattr(query_methods, operation)
    int_node_id = int(level)
    return HttpResponse(methodToCall(int_node_id, path))
