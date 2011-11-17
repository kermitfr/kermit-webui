'''
Created on Aug 10, 2011

@author: mmornati
'''
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson as json
import logging
from webui.restserver.utils import Actions
from webui.restserver.communication import callRestServer
from webui.restserver.template import render_agent_template
from django.contrib.auth.decorators import login_required
from guardian.decorators import permission_required
from webui.agent.utils import verify_agent_acl, verify_action_acl

logger = logging.getLogger(__name__)

#Added security on each method. In this way, even if user try to call mcollective directly using url
#the acls are verified after call.
#User must have "call_mcollective" to enter methods and then must have acl on agent and method he need to call

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def get(request, filters, agent, action, args=None):
    if verify_agent_acl(request.user, agent) and verify_action_acl(request.user, agent, action):
        response, content = callRestServer(request.user, filters, agent, action, args)
        if response.status == 200:
            json_data = render_agent_template(request, {}, content, {}, agent, action)
            return HttpResponse(json_data, mimetype="application/json")
        return response
    else:
        return HttpResponseForbidden()

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def getWithTemplate(request, template, filters, agent, action, args=None):
    if verify_agent_acl(request.user, agent) and verify_action_acl(request.user, agent, action):
        response, content = callRestServer(request.user, filters, agent, action, args)
        if response.status == 200:
            jsonObj = json.loads(content)
            templatePath = 'ajax/' + template + '.html'
            data = {
                    'content': jsonObj
            }
            return render_to_response( templatePath, data,
                context_instance = RequestContext( request ) )
        return response
    else:
        return HttpResponseForbidden()
        

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def executeAction(request, action, type='SYNC'):
    logger.info("Executing action " + action)
    actions = Actions()
    actionToExecute = getattr(actions, action)
    if type == 'ASYNC':
        result = actionToExecute(request.user)
    else:
        actionToExecute(request.user)
        result = json.dumps({'result': ''})
    return HttpResponse(result, mimetype="application/json")
    
@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def executeGeneralAction(request, action, filter, type):
    logger.info("Executing action " + action)
    actions = Actions()
    actionToExecute = getattr(actions, action)
    actionToExecute(request.user, filter, type)
    return HttpResponse('')
        

