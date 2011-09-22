'''
Created on Sep 9, 2011

@author: mmornati
'''
from webui.restserver.communication import callRestServer
from django.utils import simplejson as json
import logging
from webui.puppetclasses.models import PuppetClass
from webui.serverstatus.models import Server
from webui.platforms import settings as platform_settings
import imp

logger = logging.getLogger(__name__)

def get_apps_list(user, filters, file_type):
    logger.debug("Calling app_list with filters %s and type %s" % (filters, str(file_type)))
    try: 
        response, content = callRestServer(user, filters, "a7xdeploy", "applist", "apptype="+str(file_type))
        if response.status == 200:
            jsonObj = json.loads(content)
            if jsonObj:
                #Looking for "intersections"
                app_list = None
                for server_response in jsonObj:
                    if not app_list:
                        app_list = server_response['data']['applist']
                    else:
                        app_list = set(app_list).intersection(server_response['data']['applist'])
                return json.dumps({"errors":"", "applist":app_list})
            else:
                return json.dumps({"errors":"Cannot retrieve apps list"})
    except Exception, err:  
        logger.error('ERROR: ' + str(err))
        

def retrieve_instances(filters, type):
    logger.debug("Extracting servers from filters to retrieve instances")
    classes = []
    server_selected = None
    class_list = filters.split(';')
    for puppet_class in class_list:
        current_filter = puppet_class.split('=')
        if current_filter[0] == 'class_filter':
            classes.append(PuppetClass.objects.get(name=current_filter[1]))
        else: 
            server_selected = Server.objects.get(fqdn=current_filter[1])
    logger.debug("Classes found in your filter: %s" % str(classes))
    logger.debug("Server selected with your filter: %s" % server_selected)
    servers_list = []
    if classes:
        logger.debug("Retrieving server using classes")
        servers_list = Server.objects.filter(puppet_classes__in = classes, deleted=False)
    else:
        servers_list.append(server_selected)
        
    logger.debug("Retrieving instances for selected server")
    for platform in platform_settings.INSTALLED_PLATFORMS:
        if not platform == type:
            logger.debug("Skipping %s platform! Looking for %s" % (platform, type))
            continue
        platform_name = 'webui.platforms.' + platform
        try:
            platform_path = __import__(platform_name, {}, {}, [platform_name.split('.')[-1]]).__path__
        except AttributeError:
            continue
        try:
            fp, pathname, description = imp.find_module('utils', platform_path)
            mod = imp.load_module('utils', fp, pathname, description)
            current_app_inst = []
            for server in servers_list:
                instances = mod.extract_instances_name(server.hostname)
                if current_app_inst:
                    current_app_inst = set(current_app_inst).intersection(set(instances))
                else:
                    current_app_inst = instances
            return json.dumps({"instances":list(current_app_inst)})
        except:
            logger.debug('No module utils found for %s' % platform_path)
        
    return json.dumps({"instances":[]})
