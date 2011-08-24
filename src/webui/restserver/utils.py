'''
Created on Aug 19, 2011

@author: mmornati
'''
from django.utils import simplejson as json
from datetime import datetime
from webui.serverstatus.models import Server, Agent
from webui.puppetclasses.models import PuppetClass
import logging
import httplib2
from django.conf import settings
from webui.widgets.loading import registry

logger = logging.getLogger(__name__)

def callRestServer(filters, agent, action, args=None):
    http = httplib2.Http()
    url = settings.RUBY_REST_BASE_URL
    url += filters + "/"
    url += agent + "/"
    url += action + "/"
    if args:
        url += args + "/"
    logger.info('Calling RestServer on: ' + url)
    response, content = http.request(url, "GET")
    logger.info('Response: ' + str(response))
    logger.info('Content: ' + str(content))
    return response, content

class Actions(object):

    def refresh_dashboard(self):
        logger.info("Getting all Widgets from database")
        registry.reset_cache()
        widgets_list = registry.refresh_widgets()
        for widget in widgets_list:
            retrieved = registry.get_widget(widget['name'])
            retrieved.db_reference = widget
                
    def refresh_server_basic_info(self):
        logger.info("Calling Refresh Basic Info")
        ops = Operations()
        ops.server_basic_info()
        
    def refresh_server_inventory(self):
        logger.info("Calling Refresh Inventory")
        ops = Operations()
        ops.server_inventory()

class Operations(object):
    
    def server_basic_info(self):
        try: 
            response, content = callRestServer('no-filter', 'nodeinfo', 'basicinfo')
            if response.status == 200:
                jsonObj = json.loads(content)
                update_time = datetime.now()
                for server in jsonObj:
                    #verify if server exists in database
                    server_name = server['sender']
                    #Using filter because get sometimes generates query error
                    #The filter result is a collection, so you need to select the first element to work
                    query_response = Server.objects.filter(hostname=server_name)
                    if query_response:
                        retrieved_server = query_response[0]
                        logger.info("Updating Server information " + server_name)
                        self.complete_server_info(retrieved_server, server, update_time)
                        retrieved_server.save()
                    else: 
                        logger.info("Creating new server with name " + server_name)
                        new_server = Server.objects.create(hostname=server_name)
                        self.complete_server_info(new_server, server, update_time)
                        new_server.save()
                    
                    #Retrieving not updated/created server and set them to OFFLINE
                    logger.info("Checking offline servers")
                    not_updated = Server.objects.filter(updated_time__lt=update_time)
                    for server in not_updated:
                        server.online = False
                        server.save()
                            
        except Exception, err:
            logger.error('ERROR: ' + str(err))
            
    def complete_server_info(self, server, mcresponse, update_time):
        server.online = True
        if mcresponse['data'].has_key('facts'):
            try:
                server.os = mcresponse['data']['facts']['lsbdistdescription']
            except KeyError:
                server.os = 'Unknown'
            try:
                server.architecture = mcresponse['data']['facts']['architecture']
            except KeyError:
                server.architecture = 'Unknown' 
            try:
                server.fqdn = mcresponse['data']['facts']['fqdn']
            except KeyError:
                server.fqdn = server.hostname
        else:
            server.os = 'Unknown'
            server.architecture = 'Unknown'
        server.updated_time = update_time
        #Add puppet_classes
        self.add_puppet_classes(server, mcresponse['data']['classes'])
        #Add agents
        self.add_agents(server, mcresponse['data']['agentlist'])
        #Create PuppetClass Path
        self.create_path(server, mcresponse['data']['classes'])
       
    def server_inventory(self):
        try: 
            response, content = callRestServer('no-filter', 'a7xinventory', 'oasinv')
        except Exception, err:
            logger.error('ERROR: ' + str(err))
            
    def add_puppet_classes(self, server, puppet_classes):
        for current in puppet_classes:
            retrieved = PuppetClass.objects.filter(name=current)
            if retrieved:     
                server.puppet_classes.add(retrieved[0])
            else:
                logger.warn("Cannot find class with name " + current)
                
    def add_agents(self, server, agents_list):
        for agent in agents_list:
            retrieved = Agent.objects.filter(name=agent)
            if retrieved:     
                server.agents.add(retrieved[0])
            else:
                logger.info("Discovered new agent " + agent)
                new_agent = Agent.objects.create(name=agent)
                server.agents.add(new_agent) 
    
    def create_path(self, server, puppet_classes):
        path = ''
        for i in range (0, 5):
            level_classes = PuppetClass.objects.filter(level=i).values_list('name', flat=True)
            intersection = set(puppet_classes).intersection(set(level_classes))
            if intersection:
                extracted_class = iter(intersection).next()
                if extracted_class:
                    path = path + '/' + extracted_class
        
        server.puppet_path=path
