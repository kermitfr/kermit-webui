from webui.agent.models import Agent, Action, ActionInput, ActionOutput
from webui.restserver.communication import callRestServer
import logging
from django.utils import simplejson as json

logger = logging.getLogger(__name__)


def verify_agent_acl(user, agent_name):
    agent = Agent.objects.get(name=agent_name)
    return user.has_perm('use_agent', agent)

def verify_action_acl(user, action_name):
    action = Action.objects.get(name=action_name)
    return user.has_perm('use_action', action)

def update_agents_info(user):
    agents_list = Agent.objects.filter(enabled=True)
    for agent in agents_list:
        update_info(user, agent)
        
def update_info(user, agent):
    logger.info('Calling Mcollective to get info for agent ' + agent.name)
    response, content = callRestServer(user, "limit_targets=1", "agentinfo", "desc", "agentname="+agent.name)
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
                            ActionInput.objects.create(action=saved_action, name=input_name, description=input_content['description'], type=input_content['type'], prompt=input_content['prompt'], optional=input_content['optional'], validation=input_content['validation'], max_length=input_content['maxlength'])
                        else:
                            logger.debug('Input with name ' + input_name + " already present in DB. Updating...")
                            input_to_update = input_db[0]
                            input_to_update.description=input_content['description']
                            input_to_update.type=input_content['type']
                            input_to_update.prompt=input_content['prompt']
                            input_to_update.optional=input_content['optional']
                            input_to_update.validation=input_content['validation']
                            input_to_update.max_length=input_content['maxlength']
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
