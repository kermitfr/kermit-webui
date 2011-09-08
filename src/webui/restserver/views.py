'''
Created on Aug 10, 2011

@author: mmornati
'''
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson as json
import logging
from webui.restserver.utils import Actions
from webui.restserver.communication import callRestServer
from webui.restserver.template import render_agent_template
from django.contrib.auth.decorators import login_required
from guardian.decorators import permission_required

logger = logging.getLogger(__name__)

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def get(request, filters, agent, action, args=None):
    response, content = callRestServer(filters, agent, action, args)
    if response.status == 200:
        json_data = render_agent_template(request, {}, content, {}, agent, action)
        return HttpResponse(json_data, mimetype="application/json")
    return response

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
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

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def executeAction(request, action):
    logger.info("Executing action " + action)
    actions = Actions()
    actionToExecute = getattr(actions, action)
    actionToExecute()
    return HttpResponse('')
        

