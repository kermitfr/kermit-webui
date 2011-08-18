'''
Created on Aug 16, 2011

@author: mmornati
'''

from webui.django_cron import cronScheduler, Job
import logging
from webui.restserver.views import callRestServer
from django.utils import simplejson as json
from webui.serverstatus.models import Server, Agent
from webui.puppetclasses.models import PuppetClass
from datetime import datetime

logger = logging.getLogger(__name__)

class UpdateServerStatus(Job):
        """
        Cron Job that calls mcollective updating server status in app db
        """
        
        #run every n seconds
        run_every = 3600

        def job(self):
            logger.info("Running Job UpdateServerStatus")
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
                            self.add_puppet_classes(retrieved_server, server['data']['classes'])
                            #Add agents
                            self.add_agents(retrieved_server, server['data']['agentlist'])
                            #Create PuppetClass Path
                            self.create_path(retrieved_server, server['data']['classes'])
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
                            self.add_puppet_classes(new_server, server['data']['classes'])
                            #Add agents
                            self.add_agents(new_server, server['data']['agentlist'])
                            #Create PuppetClass Path
                            self.create_path(new_server, server['data']['classes'])

                            new_server.save()
                        
                        #Retrieving not updated/created server and set them to OFFLINE
                        logger.info("Checking offline servers")
                        not_updated = Server.objects.filter(updated_time__lt=update_time)
                        for server in not_updated:
                            server.online = False
                            server.save()
                       
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
                extracted_class = iter(set(puppet_classes).intersection(set(level_classes))).next()
                if extracted_class:
                    path = path + '/' + extracted_class
            
            server.puppet_path=path
                
                
cronScheduler.register(UpdateServerStatus)

