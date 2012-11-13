'''
Created on Nov 9, 2012

@author: mmornati
'''
from celery.task import task
import logging
from webui.restserver.communication import callRestServer
from webui.messages.models import Message
from webui.servers.models import Server

logger = logging.getLogger(__name__)

@task()
def check_kermit_base_agents(user):
    #Execute PING Mco Operation
    check_kermit_base_agents.update_state(state="PROGRESS", meta={"current": 0, "total": 100})
    response, content = callRestServer(user, None, "rpcutil", "ping", use_task=False)
    if response.getStatus() == 200:
        ping_list = []
        for resp in content:
            ping_list.append(resp.getSender())
        logger.debug("Ping List: %s" % ping_list)

        logger.debug("Executing PING with agent=nodeinfo filter")
        check_kermit_base_agents.update_state(state="PROGRESS", meta={"current": 25, "total": 100})
        response, content_nodeinfo = callRestServer(user, "agent=nodeinfo", "rpcutil", "ping", use_task=False)
        nodeinfo_list = []
        for resp in content_nodeinfo:
            nodeinfo_list.append(resp.getSender())
        logger.debug("NodeInfo List: %s" % nodeinfo_list)
        
        logger.debug("Executing PING with agent=agentinfo filter")
        check_kermit_base_agents.update_state(state="PROGRESS", meta={"current": 50, "total": 100})
        response, content_agentinfo = callRestServer(user, "agent=agentinfo", "rpcutil", "ping", use_task=False)
        agentinfo_list = []
        for resp in content_agentinfo:
            agentinfo_list.append(resp.getSender())
        logger.debug("AgentInfo List: %s" % agentinfo_list)    
            
        logger.debug("Verify pings responses")
        servers_without_nodeinfo = list(ping_list)
        try: 
            [servers_without_nodeinfo.remove(x) for x in nodeinfo_list]
        except Exception, e:
            logger.error("Error in servers lists: %s" % str(e))
            servers_without_nodeinfo = []
        
        servers_without_agentinfo = list(ping_list)
        try:
            [servers_without_agentinfo.remove(x) for x in agentinfo_list]
        except Exception, e:
            logger.error("Error in servers lists: %s" % str(e))
            servers_without_agentinfo = []
        
        both_two_agents = list(set(servers_without_agentinfo).intersection(servers_without_nodeinfo))
        try:
            [servers_without_agentinfo.remove(x) for x in both_two_agents]
            [servers_without_nodeinfo.remove(x) for x in both_two_agents]
        except Exception, e:
            logger.error("Error in servers lists: %s" % str(e))
            servers_without_agentinfo = []
            servers_without_nodeinfo = []
            
        logger.debug("Server Without Two Agents: %s" % both_two_agents)
        logger.debug("Server Without AgentInfo: %s" % servers_without_agentinfo)
        logger.debug("Server Without AgentInfo: %s" % servers_without_nodeinfo)
        
        #TODO: Check if there is an ignore message
        #Else Add message
        for server in both_two_agents:
            text_message = "Nodeinfo and Agentinfo mco agents not installed!"
            try:
                server_db = Server.objects.get(hostname=server)
            except:
                try: 
                    server_db = Server.objects.get(fqdn=server)
                except: 
                    logger.warn("No server found in Database. Creating new entry without information...")
                    server_db = Server.objects.create(hostname=server, fqdn=server)
             
            Message.custom_objects.create_message(server=server_db, level=2, message=text_message)
                
        
        for server in servers_without_agentinfo:
            text_message = "Agentinfo mco agent not installed!"
            try:
                server_db = Server.objects.get(hostname=server)
            except:
                try: 
                    server_db = Server.objects.get(fqdn=server)
                except: 
                    logger.warn("No server found in Database. Creating new entry without information...")
                    server_db = Server.objects.create(hostname=server, fqdn=server)
                    Message.objects.create(server=server_db, level=1, message="Execute ServerBasic Info operation to retrieve all server informations!")
            
            Message.custom_objects.create_message(server=server_db, level=2, message=text_message)
            
        for server in servers_without_nodeinfo:
            text_message="Nodeinfo mco agent not installed!"
            try:
                server_db = Server.objects.get(hostname=server)
            except:
                try: 
                    server_db = Server.objects.get(fqdn=server)
                except: 
                    logger.warn("No server found in Database. Creating new entry without information...")
                    server_db = Server.objects.create(hostname=server, fqdn=server)
                    continue
            
            Message.custom_objects.create_message(server=server_db, level=2, message=text_message)
        
        check_kermit_base_agents.update_state(state="PROGRESS", meta={"current": 75, "total": 100})
    else:
        logger.info("No response from PING Message check ")
        
        
    check_kermit_base_agents.update_state(state="COMPLETED", meta={"current": 100, "total": 100})
