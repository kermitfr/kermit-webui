'''
Created on Aug 10, 2011

@author: mmornati
'''
import httplib2
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson as json
import logging
from webui.widgets.loading import registry
from datetime import datetime
from webui.serverstatus.models import Server, Agent
from webui.puppetclasses.models import PuppetClass

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

def get(request, filters, agent, action, args=None):
    response, content = callRestServer(filters, agent, action, args)
    if response.status == 200:
        return HttpResponse(content, mimetype="application/json")
    return response

def getWithTemplate(request, template, filters, agent, action, args=None):
    response, content = callRestServer(filters, agent, action, args)
    if response.status == 200:
        jsonObj = json.loads(content)
        templatePath = 'ajax/' + template + '.html'
        data = {
                'content': jsonObj
        }
        return render_to_response( templatePath, data,
            context_instance = RequestContext( request ) )
    return response


def executeAction(request, action):
    logger.info("Executing action " + action)
    actions = Actions()
    actionToExecute = getattr(actions, action)
    actionToExecute()
    return HttpResponse('')

def server_inventory():
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
                    retrieved_server.online = True
                    retrieved_server.os = server['data']['facts']['lsbdistdescription']
                    retrieved_server.architecture = server['data']['facts']['architecture']
                    retrieved_server.updated_time = update_time
                    #Add puppet_classes
                    add_puppet_classes(retrieved_server, server['data']['classes'])
                    #Add agents
                    add_agents(retrieved_server, server['data']['agentlist'])
                    #Create PuppetClass Path
                    create_path(retrieved_server, server['data']['classes'])
                    retrieved_server.save()
                else: 
                    logger.info("Creating new server with name " + server_name)
                    new_server = Server.objects.create(hostname=server_name)
                    print server['data']['facts']['lsbdistdescription']
                    print server['data']['facts']['architecture']
                    new_server.os = server['data']['facts']['lsbdistdescription']
                    new_server.architecture = server['data']['facts']['architecture']
                    new_server.online = True
                    new_server.updated_time = update_time
                    #Add puppet_classes
                    add_puppet_classes(new_server, server['data']['classes'])
                    #Add agents
                    add_agents(new_server, server['data']['agentlist'])
                    #Create PuppetClass Path
                    create_path(new_server, server['data']['classes'])

                    new_server.save()
                
                #Retrieving not updated/created server and set them to OFFLINE
                logger.info("Checking offline servers")
                not_updated = Server.objects.filter(updated_time__lt=update_time)
                for server in not_updated:
                    server.online = False
                    server.save()
                        
    except Exception, err:
        logger.error('ERROR: ' + str(err))
            
            
            
def add_puppet_classes(server, puppet_classes):
    for current in puppet_classes:
        retrieved = PuppetClass.objects.filter(name=current)
        if retrieved:     
            server.puppet_classes.add(retrieved[0])
        else:
            logger.warn("Cannot find class with name " + current)
            
def add_agents(server, agents_list):
    for agent in agents_list:
        retrieved = Agent.objects.filter(name=agent)
        if retrieved:     
            server.agents.add(retrieved[0])
        else:
            logger.info("Discovered new agent " + agent)
            new_agent = Agent.objects.create(name=agent)
            server.agents.add(new_agent) 

def create_path(server, puppet_classes):
    path = ''
    for i in range (0, 5):
        level_classes = PuppetClass.objects.filter(level=i).values_list('name', flat=True)
        extracted_class = iter(set(puppet_classes).intersection(set(level_classes))).next()
        if extracted_class:
            path = path + '/' + extracted_class
    
    server.puppet_path=path

class Actions(object):

    def refresh_dashboard(self):
        logger.info("Getting all Widgets from database")
        registry.reset_cache()
        widgets_list = registry.get_widgets_dashboard()
        for key, widgets in widgets_list.items():
            for widget in widgets:
                retrieved = registry.get_widget(widget['name'])
                retrieved.db_reference = widget
                
    def refresh_server_inventory(self):
        logger.info("Calling Refresh Inventory")
        server_inventory()
        

