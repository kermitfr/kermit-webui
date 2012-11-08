'''
Created on Aug 26, 2011

@author: mmornati
'''

from django.template.base import TemplateDoesNotExist
from webui import settings
from django.template.loader import render_to_string, get_template
from django.utils import simplejson as json
import logging
from webui.agent.models import Agent, Action
from django.template.context import RequestContext

logger = logging.getLogger(__name__)

def render_agent_template(request, resp_dict, content, form_data, agent, action):
    jsonObj = json.loads(content)
    try:
        template_name = 'agents/'+agent+'/'+action+'.html'
        get_template(template_name)
        rendered_template = render_to_string(template_name, {'settings':settings, 'content': jsonObj, 'agent': agent, 'action': action, 'arguments':form_data, 'page_context': RequestContext( request )})
        resp_dict.update({'response': rendered_template, 'type':'html', 'state':'SUCCESS'})
    except TemplateDoesNotExist, e:
        try:
            logger.debug('No template found for ' + agent + ' - ' + action + '! Using default agent template')
            template_name = 'agents/default.html'
            get_template(template_name)
            logger.debug('Getting DDL output information')
            outputs = get_action_outputs(agent, action)
            if outputs:
                rendered_template = render_to_string(template_name, {'settings':settings, 'content': jsonObj, 'outputs':outputs,'agent': agent, 'action': action, 'arguments':form_data, 'page_context': RequestContext( request )})
                resp_dict.update({'response': rendered_template, 'type':'html', 'state':'SUCCESS'})
            else:
                logger.debug('No DDL outputs found for ' + agent + ' ' + action + '. Send default JSON')
                resp_dict.update({'response': jsonObj, 'type':'json', 'state':'SUCCESS'})
        except:
            logger.debug('No template found for ' + agent + ' - ' + action + '! Using default JSON viewer')
            resp_dict.update({'response': jsonObj, 'type':'json', 'state':'SUCCESS'})
                
            # Make a json whatsit to send back.
    json_data = json.dumps(resp_dict, ensure_ascii=False)
    return json_data

def get_action_inputs(agent, action):
    agent_db = Agent.objects.get(name=agent)
    if agent_db:
        action_db = Action.objects.get(name=action, agent=agent_db)
        if action_db:
                if len(action_db.inputs.values()) > 0:
                    return action_db.inputs.values()
    return None

def get_inputs(agent, action):
    inputs = get_action_inputs(agent, action)
    #Adding inputs for any operation: 
    # * Use Scheduler
    # * applying filters
    if inputs == None:
        inputs = []
    else:
        inputs = list(inputs)
        
    inputs.append({'prompt': 'Identity filter', 
                    'description': 'Identity filter', 
                    'optional': True, 
                    'max_length': 600, 
                    'validation': '.', 
                    'type': 'string', 
                    'name': 'identityfilter'})
    
    inputs.append({'prompt': 'Class filter', 
                    'description': 'Class filter', 
                    'optional': True, 
                    'max_length': 600, 
                    'validation': '.', 
                    'type': 'string', 
                    'name': 'classfilter'})
        
    inputs.append({'prompt': 'Compound filter', 
                    'description': 'Expression to apply as filter', 
                    'optional': True, 
                    'max_length': 600, 
                    'validation': '.', 
                    'type': 'string', 
                    'name': 'compoundfilter'})
    
    inputs.append({'prompt': 'Limit', 
                    'description': 'Apply limit to request', 
                    'optional': True, 
                    'max_length': 10, 
                    'validation': '.', 
                    'type': 'string', 
                    'name': 'limit'})
    
    inputs.append({'prompt': 'Use backend scheduler', 
                    'description': 'Execute operation using backend scheduler', 
                    'optional': True, 
                    'max_length': 1, 
                    'validation': '.', 
                    'type': 'boolean', 
                    'name': 'usesched'})
    
    return inputs
        
        

def get_action_outputs(agent, action):
    agent_db = Agent.objects.get(name=agent)
    if agent_db:
        action_db = Action.objects.get(name=action, agent=agent_db)
        if action_db:
                if len(action_db.outputs.values()) > 0:
                    output_dict = {}
                    for out in action_db.outputs.values():
                        output_dict[out['name']] = out['display_as']
                        
                    return output_dict
    return None

