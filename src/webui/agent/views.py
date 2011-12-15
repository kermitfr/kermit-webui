from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import simplejson as json
import logging
from webui.agent.models import Agent
from django.template.loader import render_to_string
from webui.agent.form import create_action_form
from django.template.context import RequestContext
from webui.restserver.communication import callRestServer
from webui.restserver.template import render_agent_template, get_action_inputs
from django.contrib.auth.decorators import login_required
from guardian.shortcuts import get_objects_for_user
from guardian.decorators import permission_required
from django.core.urlresolvers import reverse
from webui import settings

logger = logging.getLogger(__name__)

class QueryMethods(object):
    
    def get_action_tree(self, request, agent, action, filters, dialog_name, response_container):
        agents = Agent.objects.filter(enabled=True)
        if not request.user.is_superuser:
            agents = get_objects_for_user(request.user, 'use_agent', Agent).filter(enabled=True)
        data = []
        for agent in agents:
            db_actions = agent.actions
            actions = []
            for action in db_actions.iterator():
                if request.user.has_perm('use_action', action):
                    actions.append(action)
            if len(actions) > 0:
                content = {"isFolder": "true", "title": agent.name, "key":agent.name}
                children = []
                for action in actions:
                    action_data = {"title": action.name, "key":action.name, "agent":agent.name}
                    children.append(action_data)
                content['children'] = children
                data.append(content)
            else:
                logger.info("Excluding agent " + agent.name + " because there aren't DDL information saved. Try to update in admin area")
             
        return json.dumps(data)
    
    def get_dialog_form(self, request, agent, action, filters, dialog_name, response_container):
        inputs = get_action_inputs(agent, action)
        if inputs:
            logger.debug('Rendering form')
            form = create_action_form(inputs)
            return render_to_string('widgets/agent/modalform.html', {'agent':agent, 'action':action, 'filters':filters, 'form':form(), 'dialog_name': dialog_name, 'response_container': response_container}, context_instance=RequestContext(request))
        else:
            logger.debug('No parameters required')
            return None
        return None      
     
@login_required()    
@permission_required('agent.call_mcollective', return_403=True)
def query(request, operation, agent=None, action=None, filters='no-filter', dialog_name=None, response_container=None):
    query_methods = QueryMethods()
    methodToCall = getattr(query_methods, operation)
    return HttpResponse(methodToCall(request, agent, action, filters, dialog_name, response_container))

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def execute_action_form(request, agent, action, filters, dialog_name, response_container, xhr=None):
    if request.method == "POST":
        inputs = get_action_inputs(agent, action)
        logger.debug("Recreating form")
        form_type = create_action_form(inputs)
        form = form_type(request.POST)

        #Check if the <xhr> var had something passed to it.
        if xhr == "xhr":
            # Yup, this is an Ajax request.
            # Validate the form:
            clean = form.is_valid()
            # Make some dicts to get passed back to the browser
            rdict = {'bad':'false', 'agent':agent, 'action':action, 'dialog_name':dialog_name, 'response_container':response_container, 'filters':filters }
            if not clean:
                rdict.update({'bad':'true'})
                d = {}
                # This was painful, but I can't find a better way to extract the error messages:
                for e in form.errors.iteritems():
                    d.update({e[0]:unicode(e[1])}) # e[0] is the id, unicode(e[1]) is the error HTML.
                # Bung all that into the dict
                rdict.update({'errs': d })
                # Make a json whatsit to send back.
                json_data = json.dumps(rdict, ensure_ascii=False)
            else:
                logger.debug("Parameters check: OK.")
                logger.debug("Creating args")
                arguments=None
                for input in inputs:
                    if form.cleaned_data[input['name']]:
                        if arguments:
                            arguments = arguments + ';'
                        else:
                            arguments = ''
                        arguments = arguments + input['name'] + '=' + form.cleaned_data[input['name']] 
                
                logger.debug("Arguments for MCollective call %s" % arguments)
                wait_for_response = False
                response, content = callRestServer(request.user, filters, agent, action, arguments, wait_for_response)
                #Leave wait for response check it to support both two in the future (read wait_for_response from config file)
                if wait_for_response:
                    if response.status == 200:
                        json_data = render_agent_template(request, rdict, content, form.cleaned_data, agent, action)
                        return HttpResponse(json_data, mimetype='application/javascript')
                    else:
                        rdict.update({"result": "KO", "message": "Error communicating with server. <br> %s"%content})
                else: 
                    logger.debug("Returning request UUID")
                    update_url = reverse('get_progress', kwargs={'taskname':content, 'taskid':response.task_id})
                    rdict.update({"UUID": response.task_id, "taskname": content, 'update_url': update_url})
             
            return HttpResponse(json.dumps(rdict, ensure_ascii=False), mimetype='application/javascript')
        else:
            if form.is_valid():
                logger.error("Trying to execute a NON Ajax call. Rejected and redirected to DashBoard.")
                return HttpResponseRedirect(settings.BASE_URL)
    else:
        # It's not post so make a new form
        logger.warn("Cannot access this page using GET")
        raise Http404