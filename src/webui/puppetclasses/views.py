from django.http import HttpResponse
from webui.puppetclasses.models import PuppetClass
from django.utils import simplejson as json
import logging
from webui.serverstatus.models import Server

logger = logging.getLogger(__name__)

class QueryMethods():
    
    def get_children(self, id):
        logger.info("Calling get_children method with id: " + str(id))
        parent = ''
        if id == -1:
            parent = None
        else:
            parent = id
            
        #Call for parent
        classes = PuppetClass.objects.filter(enabled=True, parent=parent)
        data = []
        for puppetclass in classes:
            children = self.get_child_data(puppetclass)
            content = {"progressive_render": "true", "data": puppetclass.name, "attr":{"id":puppetclass.pk, "rel":"folder"}, "children":children}
            data.append(content)
             
        return json.dumps(data)
    
    def get_child_data(self, current_node):
        childlist = []
        for child in current_node.children.all():
            children = self.get_child_data(child)
            childata = {"data":child.name, "attr":{"id":child.pk, "rel":"folder"}, "children":children}
            childlist.append(childata) 
           
        if len(childlist) == 0:
            logger.info("Retrieving servers contained in class " + current_node.name)
            #Getting server in current class
            servers = Server.objects.filter(puppet_classes=current_node)
            for server in servers:
                childata = {"data":server.hostname, "attr":{"id":server.pk, "rel":"default"}}
                childlist.append(childata) 
            
        return childlist
        
def query(request):
    operation = request.GET['operation']
    node_id = request.GET['id']
    query_methods = QueryMethods()
    methodToCall = getattr(query_methods, operation)
    int_node_id = int(node_id)
    return HttpResponse(methodToCall(int_node_id))
