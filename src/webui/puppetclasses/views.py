from django.http import HttpResponse
from webui.puppetclasses.models import PuppetClass
from django.utils import simplejson as json
import logging
from webui.serverstatus.models import Server
from django.contrib.auth.decorators import login_required
from guardian.shortcuts import get_objects_for_user
from webui import settings

logger = logging.getLogger(__name__)

class QueryMethods(object):
    
    def generate_tree(self, user, classes, level, path):
        data = []
        for puppetclass in classes:
            test_path=path+'/'+puppetclass.name
            #Retrieving all sub classes
            servers_list = Server.objects.filter(puppet_classes = puppetclass, deleted=False)
            if (servers_list):
                content = {"isFolder": "true", "isLazy": "false", "title": puppetclass.name, "level":puppetclass.level, "key":puppetclass.name, "filtername":puppetclass.name}
                children = []
                sub_classes = PuppetClass.objects.filter(enabled=True, level=level+1)
                if sub_classes:
                    children.append(self.generate_tree(user, sub_classes, level+1, test_path))

                #We cannot use / inside rest url, so / was substituted by _
                #Here we revert this change to obtain a correct path
                logger.info("Looking for servers in path: " + path)
                servers = Server.objects.filter(puppet_path=path, deleted=False)
                if user != 'fooUser':
                        if not user.is_superuser and settings.FILTERS_SERVER:
                            servers = get_objects_for_user(user, 'use_server', Server).filter(puppet_path=path, deleted=False)
                for server in servers:
                    serverdata = {"title":server.fqdn, "url": settings.BASE_URL + "/server/details/"+server.hostname+"/", "key":server.fqdn, "filtername":server.hostname}
                    children.append(serverdata)
                
                content['children'] = children
                data.append(content)
        
        return data
        
    def get_all_tree(self, user, level, unused_path):
        logger.info("Generint all classes tree")
        path = ''
        if settings.FILTERS_CLASS:
            classes = get_objects_for_user(user, 'access_puppet_class', PuppetClass).filter(enabled=True, level=level)
        else:
            classes = PuppetClass.objects.filter(enabled=True, level=level)
        data = self.generate_tree(user, classes, 0, path)
        
        #We cannot use / inside rest url, so / was substituted by _
        #Here we revert this change to obtain a correct path
        logger.info("Looking for servers in path: " + path)
        servers = Server.objects.filter(puppet_path=path, deleted=False)
        if user != 'fooUser':
                if not user.is_superuser and settings.FILTERS_SERVER:
                    servers = get_objects_for_user(user, 'use_server', Server).filter(puppet_path=path, deleted=False)
        for server in servers:
            serverdata = {"title":server.fqdn, "url": settings.BASE_URL + "/server/details/"+server.hostname+"/", "key":server.fqdn, "filtername":server.hostname}
            data.append(serverdata)
             
        return json.dumps(data)
        
    def get_tree_nodes(self, user, level, path):
        logger.info("Calling get_tree_nodes for level: " + str(level))
        if settings.FILTERS_CLASS:
            classes = get_objects_for_user(user, 'access_puppet_class', PuppetClass).filter(enabled=True, level=level+1)
        else:
            classes = PuppetClass.objects.filter(enabled=True, level=level+1)
        data = []
        if path:
            path = path.replace('_', '/')
        else:
            path = ''
        for puppetclass in classes:
            test_path=path+'/'+puppetclass.name
            servers = Server.objects.filter(puppet_path__startswith=test_path)
            if user != 'fooUser':
                if not user.is_superuser and settings.FILTERS_SERVER:
                    servers = get_objects_for_user(user, 'use_server', Server).filter(puppet_path__startswith=test_path)
            if len(servers)>0:
                content = {"isFolder": "true", "isLazy": "false", "title": puppetclass.name, "level":puppetclass.level, "key":puppetclass.name, "filtername":puppetclass.name}
                data.append(content)
            else:
                logger.info("Excluding class " + str(puppetclass) + " because there are no server inside")
        
        #We cannot use / inside rest url, so / was substituted by _
        #Here we revert this change to obtain a correct path
        logger.info("Looking for servers in path: " + path)
        servers = Server.objects.filter(puppet_path=path, deleted=False)
        if user != 'fooUser':
                if not user.is_superuser and settings.FILTERS_SERVER:
                    servers = get_objects_for_user(user, 'use_server', Server).filter(puppet_path=path, deleted=False)
        for server in servers:
            serverdata = {"title":server.fqdn, "url": settings.BASE_URL + "/server/details/"+server.hostname+"/", "key":server.fqdn, "filtername":server.hostname}
            data.append(serverdata)
             
        return json.dumps(data)
 
@login_required()       
def query(request, operation, level, path=None):
    query_methods = QueryMethods()
    methodToCall = getattr(query_methods, operation)
    int_node_id = int(level)
    return HttpResponse(methodToCall(request.user, int_node_id, path))
