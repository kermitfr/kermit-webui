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
from django.core.urlresolvers import reverse
import djcelery
from django.template.loader import render_to_string
import ast
import sys

logger = logging.getLogger(__name__)

#Added security on each method. In this way, even if user try to call mcollective directly using url
#the acls are verified after call.
#User must have "call_mcollective" to enter methods and then must have acl on agent and method he need to call

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def get(request, filters, agent, action, args=None, wait_for_response=False):
    if verify_agent_acl(request.user, agent) and verify_action_acl(request.user, agent, action):
        response, content = callRestServer(request.user, filters, agent, action, args, wait_for_response)
        if wait_for_response:
            if response.status == 200:
                json_data = render_agent_template(request, {}, content, {}, agent, action)
                return HttpResponse(json_data, mimetype="application/json")
        else:
            logger.debug("Returning request UUID")
            update_url = reverse('get_progress', kwargs={'taskname':content, 'taskid':response.task_id})
            json_data = json.dumps({"UUID": response.task_id, "taskname": content, 'update_url': update_url})
            return HttpResponse(json_data, mimetype="application/json")
    else:
        return HttpResponseForbidden()

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def getWithTemplate(request, template, filters, agent, action, args=None):
    if verify_agent_acl(request.user, agent) and verify_action_acl(request.user, agent, action):
        response, content = callRestServer(request.user, filters, agent, action, args, True)
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

@login_required()
def get_task_info(request, uuid):
    logger.debug("Retrieving task %s information" % uuid)
    celery_task = djcelery.models.TaskState.objects.get(task_id=uuid)
    arguments_list = ast.literal_eval(celery_task.args)
    if len(arguments_list) == 4:
        arguments = {"filter":arguments_list[0],
                     "agent": arguments_list[1],
                     "action": arguments_list[2],
                     "arguments": arguments_list[3]}
    else:
        arguments = {"filter":"",
                     "agent": "",
                     "action": "",
                     "arguments": ""}
    response_list = ast.literal_eval(celery_task.result)
    if len(response_list) > 2:
        try:
            content = ast.literal_eval(response_list[1])
        except:
            logger.debug("String stored is in JSON format and not a python object")
            content = json.loads(response_list[1])
        response = {"response": response_list[0],
                    "content": content}
    else:
        response = {"response": "", "content": ""}
    
    return HttpResponse(render_to_string('widgets/restserver/jobdetails.html', {'task': celery_task, "jobarg": arguments, "response": response}, context_instance=RequestContext(request)))

