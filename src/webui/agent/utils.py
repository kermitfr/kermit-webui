from webui.agent.models import Agent, Action, ActionInput, ActionOutput
from webui.restserver.communication import callRestServer
import logging
from django.utils import simplejson as json
from webui.serverstatus.models import Server

logger = logging.getLogger(__name__)


def verify_agent_acl(user, agent_name):
    try:
        agent = Agent.objects.get(name=agent_name)
        return user.has_perm('use_agent', agent)
    except:
        return False

def verify_action_acl(user, agent_name, action_name):
    try:
        agent = Agent.objects.get(name=agent_name)
        action = Action.objects.get(name=action_name, agent=agent)
        return user.has_perm('use_action', action)
    except:
        return False
        
def update_info(user, agent):
    logger.info('Calling Mcollective to get info for agent ' + agent.name)
    #Extract n servers containing the agent
    servers_list = Server.objects.filter(agents=agent, deleted=False)
    filters = None
    for current in servers_list:
        filters = "identity_filter=%s" % current.hostname
        break;
    response, content = callRestServer(user, filters, "agentinfo", "desc", "agentname="+agent.name)
    if response['status'] == '200':
        json_content = json.loads(content)
        for msg in json_content:
            if msg['statusmsg'] == 'OK':
                #Verifying Action. If already present in DB just update it
                for action_name, action_content in msg['data']['actionhash'].items():
                    action_db = Action.objects.filter(name=action_name, agent=agent)
                    saved_action = None
                    if len(action_db) == 0:
                        logger.debug('Creating Action ' + action_name)
                        saved_action = Action.objects.create(name=action_name, description=action_name, agent=agent)
                    else:
                        saved_action = action_db[0]
                    
                    #Verifying Action Inputs. If already present in DB just update it
                    for input_name, input_content in action_content['input'].items():
                        input_db = ActionInput.objects.filter(name=input_name, action=saved_action)
                        if len(input_db) == 0:
                            logger.debug('Creating Action Inputs')
                            validation = None
                            maxlenght = None
                            if 'validation' in input_content:
                                validation=input_content['validation']
                            if 'maxlength' in input_content:
                                maxlenght=input_content['maxlength']
                            ActionInput.objects.create(action=saved_action, name=input_name, description=input_content['description'], type=input_content['type'], prompt=input_content['prompt'], optional=input_content['optional'], validation=validation, max_length=maxlenght  )
                        else:
                            logger.debug('Input with name ' + input_name + " already present in DB. Updating...")
                            input_to_update = input_db[0]
                            input_to_update.description=input_content['description']
                            input_to_update.type=input_content['type']
                            input_to_update.prompt=input_content['prompt']
                            input_to_update.optional=input_content['optional']
                            if 'validation' in input_content:
                                input_to_update.validation=input_content['validation']
                            else:
                                input_to_update.validation=None
                            if 'maxlength' in input_content:
                                input_to_update.max_length=input_content['maxlength']
                            else:
                                input_to_update.max_length=None
                            input_to_update.save()
                    
                    #Verifying Action Outputs. If already present in DB just update it
                    for output_name, output_content in action_content['output'].items():
                        output_db = ActionOutput.objects.filter(name=output_name, action=saved_action)
                        if len(output_db) == 0:
                            logger.debug('Creating Action Outputs')
                            ActionOutput.objects.create(action=saved_action, name=output_name, description=output_content['description'], display_as=output_content['display_as'])
                        else:
                            logger.debug('Output with name ' + output_name + " already present in DB. Updating...")
                            output_to_update = output_db[0]
                            output_to_update.description=output_content['description']
                            output_to_update.display_as=output_content['display_as']
                            output_to_update.save()
                            
            else:
                logger.warn("Agent " + agent.name + " as no DDL configured!!")
