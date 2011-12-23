'''
Created on Nov 26, 2011

@author: mmornati
'''
from django.contrib.auth.decorators import login_required
import logging
from django.shortcuts import render_to_response
from webui import settings
from django.template.context import RequestContext
from guardian.shortcuts import get_objects_for_user
from webui.serverstatus.models import Server
from django.http import HttpResponse, Http404
from django.utils import simplejson as json
from webui.platforms.oracledb.utils import sql_list
from webui.chain.utils import construct_filters
from guardian.decorators import permission_required
from webui.platforms.oc4j.utils import get_apps_list as oc4j_app_list
from webui.platforms.weblogic.utils import get_apps_list as weblo_app_list
from webui.platforms.bar.utils import get_available_bars
from celery.execute import send_task
from django.core.urlresolvers import reverse
from webui.chain.models import Scheduler, SchedulerTask
import sys
from datetime import datetime
import djcelery
from django.template.loader import render_to_string
import ast

logger = logging.getLogger(__name__)

@login_required
def show_page(request):
    logger.debug("Rendering Scheduler Page")
    return render_to_response('chain/chain.html', {"settings":settings,  "base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, 'service_status_url':settings.RUBY_REST_PING_URL}, context_instance=RequestContext(request))


@login_required
def server_list(request):
    servers = Server.objects.filter(deleted=False)
    if not request.user.is_superuser and settings.FILTERS_SERVER:
        servers = get_objects_for_user(request.user, 'use_server', Server).filter(deleted=False)
    server_list = []
    for server in servers:
        server_list.append({'id': server.fqdn, 'name': server.fqdn})
    return HttpResponse(json.dumps({"results":server_list}))

@login_required
@permission_required('agent.call_mcollective', return_403=True)
def execute_chain(request, xhr=None):
    if request.method == "POST":
        #Check if the <xhr> var had something passed to it.
        if xhr == "xhr":
            operations =[]
            i = 1
            errors = False
            errs = {}
            while "operation%s" % i in request.POST:
                rdict = {'bad':'false'}
                try:
                    servers = request.POST["listServerHidden%s"%i]
                    filters = construct_filters(servers)
                    rdict.update({'filters':filters})
                except:
                    errors = True
                    errs.update({"listServer%s"%i:'<ul class="errorlist"><li>You must select at least one server</li></ul>'})
                    
                
                if request.POST["operation%s"%i] == 'script_ex':
                    try:
                        sqlScript = request.POST["sqlScript%s"%i]
                        instancename = request.POST["dbinstancename%s"%i]
                    except:
                        sqlScript=None
                        instancename=None
                    if sqlScript and instancename:
                        current_op = {"user": request.user,
                                      "filters": filters,
                                      "agent": "oracledb",
                                      "action": "execute_sql",
                                      "args": "instancename=%s;sqlfile=%s" % (instancename, sqlScript),
                                      "name": "Execute SQL Script"}
                        operations.append(current_op)
                    else:
                        errors = True
                        if sqlScript==None:
                            errs.update({"sqlScript%s"%i: '<ul class="errorlist"><li>Select a valid SqlScript to execute</li></ul>'})
                        if instancename==None:
                            errs.update({"dbinstancename%s"%i:'<ul class="errorlist"><li>Database Name is required</li></ul>'})
                elif request.POST["operation%s"%i] == 'deploy_ear':
                    try:
                        appfile = request.POST['earApp%s'%i]
                        instancename = request.POST['instancename%s'%i]
                        appname = request.POST['appname%s'%i]
                        serverType = request.POST['serverType%s'%i]
                    except:
                        appname=None
                    if appfile and instancename and appname and serverType:
                        logger.debug("Parameters check: OK.")
                        logger.debug("Calling MCollective to deploy %s application on %s filtered server" % (appfile, filters))
                        agent_name = None
                        if serverType == 'OC4J':
                            agent_name = 'a7xoas'
                        elif serverType == 'WebLogic':
                            agent_name = 'a7xows'
                        current_op = {"user": request.user,
                                  "filters": filters,
                                  "agent": agent_name,
                                  "action": "deploy",
                                  "args": "appname=%s;instancename=%s;appfile=%s" %(appname, instancename, appfile),
                                    "name": "Deploy Application"}
                        operations.append(current_op)
                    else:
                        errors = True 
                        if appfile==None:
                            errs.update({"earApp%s"%i: '<ul class="errorlist"><li>Application to deploy is required</li></ul>'})
                        if instancename==None:
                            errs.update({"instancename%s"%i:'<ul class="errorlist"><li>Instance Name is required</li></ul>'})
                        if appname==None:
                            errs.update({"appname%s"%i:'<ul class="errorlist"><li>Application Name is required</li></ul>'})
                        if serverType==None:
                            errs.update({"serverType%s"%i:'<ul class="errorlist"><li>Server Type is required</li></ul>'})
                elif request.POST["operation%s"%i] == 'deploy_bar':
                    try:
                        barapp = request.POST['barApp%s'%i]
                        consolename = request.POST['consoleName%s'%i]
                    except:
                        barapp=None
                        consolename = None
                    if barapp and consolename:
                        logger.debug("Parameters check: OK.")
                        logger.debug("Calling MCollective to deploy %s bar on %s filtered server" % (barapp, filters))
                        current_op = {"user": request.user,
                                  "filters": filters,
                                  "agent": "a7xbar",
                                  "action": "deploy",
                                  "args": 'filename=%s;bcname=%s' %(barapp, consolename),
                                  "name": "Deploy Bar"}
                        operations.append(current_op)
                    else:
                        errors = True
                        if barapp==None:
                            errs.update({"barApp%s"%i: '<ul class="errorlist"><li>BAR to deploy is required</li></ul>'})
                        if consolename==None:
                            errs.update({"consoleName%s"%i:'<ul class="errorlist"><li>Console Name is required</li></ul>'})
                elif request.POST["operation%s"%i] == 'restart_instance':
                    try:
                        instancename = request.POST['instancename%s'%i]
                        serverType = request.POST['serverType%s'%i]
                    except:
                        instancename=None
                        serverType=None
                    if instancename and serverType:
                        logger.debug("Parameters check: OK.")
                        logger.debug("Calling MCollective to restart instance %s" % (instancename))
                        if serverType == 'OC4J':
                            agent_name = 'a7xoas'
                        elif serverType == 'WebLogic':
                            agent_name = 'a7xows'
                        stop_op = {"user": request.user,
                                  "filters": filters,
                                  "agent": agent_name,
                                  "action": "stopinstance",
                                  "args": 'instancename=%s' %(instancename),
                                  "name": "Stop Instance"}
                        operations.append(stop_op)
                        start_op = {"user": request.user,
                                  "filters": filters,
                                  "agent": agent_name,
                                  "action": "startinstance",
                                  "args": 'instancename=%s' %(instancename),
                                  "name": "Start Instance"}
                        operations.append(start_op)
                    else:
                        errors = True
                        if instancename==None:
                            errs.update({"instancename%s"%i:'<ul class="errorlist"><li>Instance Name is required</li></ul>'})
                        if serverType==None:
                            errs.update({"serverType%s"%i:'<ul class="errorlist"><li>Server Type is required</li></ul>'})
                        
                i = i + 1
            if errors:
                rdict.update({'bad':'true'})
                rdict.update({'errs': errs })
            else:
                logger.debug("No errors detected. Executing %s operations." % (len(operations)))
                task_name = "webui.chain.tasks.execute_chain_ops"
                logger.debug("Store scheduler information on database")
                try:
                    sched = Scheduler.objects.create(name="%s-%s"%(request.user, datetime.now()), user=request.user, status="WAITING")
                    count = 0
                    for op in operations:
                        SchedulerTask.objects.create(order=count, scheduler=sched, name=op["name"], agent=op["agent"], action=op["action"], parameters=op["args"], filters=op["filters"], status="WAITING")
                        count = count + 1
                
                    result = send_task(task_name, [sched])
                    update_url = reverse('get_progress', kwargs={'taskname':task_name, 'taskid':result.task_id})
                    rdict.update({'UUID': result.task_id, 'taskname':task_name, 'update_url': update_url})
                except:
                    print sys.exc_info()
                    rdict.update({'bad':'true'})
        return HttpResponse(json.dumps(rdict, ensure_ascii=False), mimetype='application/javascript')
    else:
        # It's not post so make a new form
        logger.warn("Cannot access this page using GET")
        raise Http404
    
    
@login_required
@permission_required('agent.call_mcollective', return_403=True)
def get_sql_list(request, servers):
    if servers:
        filters = construct_filters(servers)
        return HttpResponse(sql_list(request.user, filters))
    else:
        return HttpResponse('')
    
@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def get_app_list(request, servers, server_type):
    if servers:
        filters = construct_filters(servers)
        if server_type == 'OC4J':
            return HttpResponse(oc4j_app_list(request.user, filters, 'ear'))
        elif server_type == 'WebLogic':
            return HttpResponse(weblo_app_list(request.user, filters, 'ear'))
    else:
        return HttpResponse('')
    
@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def get_bar_list(request, servers):
    if servers:
        filters = construct_filters(servers)
        return HttpResponse(get_available_bars(request.user, filters))
    else:
        return HttpResponse('')
    
@login_required()
def get_scheduler_details(request, name):
    logger.debug("Retrieving Scheduler %s information" % name)
    scheduler = Scheduler.objects.get(name=name)
    try:
        celery_task = djcelery.models.TaskState.objects.get(task_id=scheduler.task_uuid)
        celery_result = ast.literal_eval(celery_task.result)
        servers_response = celery_result[0]["messages"]
    except:
        logger.error("Cannot find celery task %s in database" % scheduler.task_uuid)
        servers_response = []
    tasks_list = []
    for task in scheduler.tasks.iterator():
        if task.result:
            result = ast.literal_eval(task.result)
        else:
            result = []
        task_obj = {"state": task.status,
                    "order": task.order,
                    "name": task.name,
                    "filter": task.filters,
                    "agent": task.agent,
                    "action": task.action,
                    "parameters": task.parameters,
                    "run_at": task.run_at,
                    "servers_response": result
                    }
        tasks_list.append(task_obj)
    return HttpResponse(render_to_string('widgets/chain/scheddetails.html', {'tasks': tasks_list}, context_instance=RequestContext(request)))

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def restart_failed_scheduler(request, name):
    logger.debug("Retrieving Scheduler %s information" % name)
    scheduler = Scheduler.objects.get(name=name)
    task_name = "webui.chain.tasks.execute_chain_ops"
    result = send_task(task_name, [scheduler])
    rdict = {}
    update_url = reverse('get_progress', kwargs={'taskname':task_name, 'taskid':result.task_id})
    rdict.update({'UUID': result.task_id, 'taskname':task_name, 'update_url': update_url})
    return HttpResponse(json.dumps(rdict, ensure_ascii=False), mimetype='application/javascript')