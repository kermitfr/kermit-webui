'''
Created on Nov 17, 2011

@author: mmornati
'''
from celery.decorators import task
import logging
from webui.restserver.communication import callRestServer
from datetime import datetime
from webui.serverstatus.models import Server
from webui.agent.models import Agent
from webui.puppetclasses.models import PuppetClass
from webui import settings
from webui.platforms.platforms import platforms
from webui.platforms.abstracts import UpdatePlatform

logger = logging.getLogger(__name__)


@task
def server_basic_info(user):
    try: 
        response, content = callRestServer(user, 'no-filter', 'nodeinfo', 'basicinfo', None, True, False)
        if response.getStatus() == 200:
            update_time = datetime.now()
            total_servers = len(content)
            i = 0
            for server in content:
                #verify if server exists in database
                server_name = server.getSender()
                #Using filter because get sometimes generates query error
                #The filter result is a collection, so you need to select the first element to work
                query_response = Server.objects.filter(hostname=server_name)
                if query_response:
                    retrieved_server = query_response[0]
                    logger.info("Updating Server information " + server_name)
                    complete_server_info(retrieved_server, server, update_time)
                    retrieved_server.save()
                else: 
                    logger.info("Creating new server with name " + server_name)
                    new_server = Server.objects.create(hostname=server_name)
                    complete_server_info(new_server, server, update_time)
                    new_server.save()
                
                #Retrieving not updated/created server and set them to OFFLINE
                logger.info("Checking offline servers")
                not_updated = Server.objects.filter(updated_time__lt=update_time)
                for not_updated_server in not_updated:
                    not_updated_server.online = False
                    not_updated_server.save()
                i = i + 1
                server_basic_info.update_state(state="PROGRESS", meta={"current": i, "total": total_servers})
                        
    except Exception, err:
        logger.error('ERROR: ' + str(err))
        
@task()
def server_inventory(user, updates_defined=None):
    if not updates_defined:
        logger.debug("Calling without updates. Trying to retrieve them")
        updates_defined = platforms.extract(UpdatePlatform)
        
    if updates_defined:
        total_updates = len(updates_defined)
        i = 0
        for current_update in updates_defined:
            current_update.inventoryUpdate(user, False)
            i = i + 1
            server_inventory.update_state(state="PROGRESS", meta={"current": i, "total": total_updates})
    else:
        logger.warn("No update defined for installed platforms")
        
def complete_server_info(server, mcresponse, update_time):
        server.online = True
        if mcresponse.getData().has_key('facts'):
            try:
                server.os = mcresponse.getData()['facts']['lsbdistdescription']
            except KeyError:
                server.os = 'Unknown'
            try:
                server.architecture = mcresponse.getData()['facts']['architecture']
            except KeyError:
                server.architecture = 'Unknown' 
            try:
                server.fqdn = mcresponse.getData()['facts']['fqdn']
            except KeyError:
                server.fqdn = server.hostname
        else:
            server.os = 'Unknown'
            server.architecture = 'Unknown'
        server.updated_time = update_time
        #Add puppet_classes
        add_puppet_classes(server, mcresponse.getData()['classes'])
        #Add agents
        add_agents(server, mcresponse.getData()['agentlist'])
        #Create PuppetClass Path
        create_path(server, mcresponse.getData()['classes'])
        
def add_puppet_classes(server, puppet_classes):
    server.puppet_classes.clear()
    for current in puppet_classes:
        retrieved = PuppetClass.objects.filter(name=current)
        if retrieved:     
            server.puppet_classes.add(retrieved[0])
        else:
            logger.warn("Cannot find class with name " + current)
            
def add_agents(server, agents_list):
    server.agents.clear()
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
    for i in range (0, settings.LEVELS_NUMBER):
        level_classes = PuppetClass.objects.filter(level=i).values_list('name', flat=True)
        intersection = list(set(puppet_classes).intersection(set(level_classes)))
        if intersection:
            if len(intersection)>1:
                for current_class in intersection:
                    if current_class != 'bcx':
                        extracted_class = current_class
                        break
            else:
                extracted_class = iter(intersection).next()
            if extracted_class:
                path = path + '/' + extracted_class
    
    server.puppet_path=path