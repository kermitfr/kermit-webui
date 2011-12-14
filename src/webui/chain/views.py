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
from webui.restserver.communication import callRestServer
from guardian.decorators import permission_required
from webui.platforms.oc4j.utils import get_apps_list
from webui.platforms.bar.utils import get_available_bars

logger = logging.getLogger(__name__)

@login_required
def show_page(request):
    logger.debug("Composing chain operation")
    operations = [{'id': 'script_ex', 'name': 'Execute Script'},
                  {'id': 'deploy_bar', 'name': 'Deploy Bar'},
                  {'id': 'deploy_ear', 'name': 'Deploy EAR'},
                  {'id': 'restart_instance', 'name': 'Restart Instance'}]
    return render_to_response('chain/chain.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, 'operations': operations ,'service_status_url':settings.RUBY_REST_PING_URL}, context_instance=RequestContext(request))


@login_required
def server_list(request):
    servers = Server.objects.filter(deleted=False)
    if request.user != 'fooUser':
            if not request.user.is_superuser and settings.FILTERS_SERVER:
                servers = get_objects_for_user(request.user, 'use_server', Server).filter(deleted=False)
    server_list = []
    for server in servers:
        server_list.append({'id': server.hostname, 'name': server.fqdn})
    return HttpResponse(json.dumps({"results":server_list}))

@login_required
@permission_required('agent.call_mcollective', return_403=True)
def execute_chain(request, xhr=None):
    if request.method == "POST":
        #Check if the <xhr> var had something passed to it.
        if xhr == "xhr":
            i = 1
            while "operation%s" % i in request.POST:
                servers = request.POST["listServer%s"%i]
                filters = construct_filters(servers)
                rdict = {'bad':'false', 'filters':filters }
                if request.POST["operation%s"%i] == 'script_ex':
                    sqlScript = request.POST["sqlScript%s"%i]
                    instancename = request.POST["dbinstancename%s"%i]
                    callRestServer(request.user, filters, 'oracledb', 'execute_sql', "instance=%s;sqlfile=%s" % (instancename, sqlScript), True)
                elif request.POST["operation%s"%i] == 'deploy_ear':
                    try:
                        appfile = request.POST['earApp%s'%i]
                        instancename = request.POST['instancename%s'%i]
                        appname = request.POST['appname%s'%i]
                    except:
                        appname=None
                    if appname and instancename and appname:
                        logger.debug("Parameters check: OK.")
                        logger.debug("Calling MCollective to deploy %s application on %s filtered server" % (appfile, filters))
                        response, content = callRestServer(request.user, filters, 'a7xoas', 'deploy', 'appname=%s;instancename=%s;appfile=%s' %(appname, instancename, appfile), True)
                        if response.status == 200:
                            json_content = json.loads(content)
                            rdict.update({"result%s"%i:json_content[0]["statusmsg"]})
                        else:
                            rdict.update({"result%s"%i: "Error communicating with server"})
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
                        response, content = callRestServer(request.user, filters, 'a7xbar', 'deploy', 'filename=%s;bcname=%s' %(barapp, consolename), True)
                        if response.status == 200:
                            json_content = json.loads(content)
                            rdict.update({"result%s"%i:json_content[0]["statusmsg"]})
                        else:
                            rdict.update({"result%s"%i: "Error communicating with server"})
                elif request.POST["operation%s"%i] == 'restart_instance':
                    try:
                        instancename = request.POST['instancename%s'%i]
                    except:
                        instancename=None
                    if instancename:
                        logger.debug("Parameters check: OK.")
                        logger.debug("Calling MCollective to restart instance %s" % (instancename))
                        response, content = callRestServer(request.user, filters, 'a7xaos', 'stopinstance', 'instancename=%s' %(instancename), True)
                        response, content = callRestServer(request.user, filters, 'a7xaos', 'startinstance', 'instancename=%s' %(instancename), True)
                        if response.status == 200:
                            json_content = json.loads(content)
                            rdict.update({"result%s"%i:json_content[0]["statusmsg"]})
                        else:
                            rdict.update({"result%s"%i: "Error communicating with server"})
                        
                i = i + 1
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
def get_app_list(request, servers):
    if servers:
        filters = construct_filters(servers)
        return HttpResponse(get_apps_list(request.user, filters, 'ear'))
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