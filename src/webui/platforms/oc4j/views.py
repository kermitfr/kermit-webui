import logging
from webui import settings
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from communication import read_server_info
from webui.platforms.utils import convert_keys_names, extract_servers,\
    read_file_log
from django.contrib.auth.decorators import login_required
from guardian.decorators import permission_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from webui.platforms.oc4j.utils import extract_instances_name, get_apps_list
from django.utils import simplejson as json
from webui.platforms.oc4j.forms import DeployForm, LogForm, InstanceForm,\
    PoolForm
from webui.restserver.communication import callRestServer

logger = logging.getLogger(__name__)

@login_required()
def instanceInventory(request, hostname, instance_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        instance = None 
        for server in server_info:
            if server['id'] == instance_name:
                instance = server
                break 
        if 'java_ver' in instance:
            java_version = instance["java_ver"]
        else:
            java_version = ""
            
        java_stop_options = ""
        java_start_options = ""
        oc4j_option = ""
        if 'java-stop-options' in instance:
            java_stop_options = instance['java-stop-options']
        if 'java-start-options' in instance:
            java_start_options = instance['java-start-options']
        if 'oc4j-options' in instance:
            oc4j_option = instance['oc4j-options']
        return render_to_response('platforms/oc4j/instance.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "java_stop_options":java_stop_options, "java_start_options":java_start_options, "oc4j_options":oc4j_option, "java_version":java_version, "hostname": hostname}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/oc4j/instance.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))


@login_required()
def datasourceListInventory(request, hostname, instance_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        instance = None 
        for server in server_info:
            if server['id'] == instance_name:
                instance = server
                break 
        for datasource in instance['datasource']:
            convert_keys_names(datasource)
        return render_to_response('platforms/oc4j/datasources.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "datasources": instance['datasource']}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/oc4j/datasources.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))

@login_required()
def datasourceInventory(request, hostname, instance_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        instance = None 
        for server in server_info:
            if server['id'] == instance_name:
                instance = server
                break 
        resource_name = resource_name.replace('_', '/')
        datasource = None
        for current in instance['datasource']:
            if current['name'] == resource_name:
                datasource = current
                convert_keys_names(datasource)
                break
        return render_to_response('platforms/oc4j/datasource.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "datasource": datasource}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/oc4j/datasource.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))

@login_required()
def applicationInventory(request, hostname, instance_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        instance = None 
        for server in server_info:
            if server['id'] == instance_name:
                instance = server
                break
        selected_app = None 
        for app in instance['applilist']:
            if app['name'] == resource_name:
                selected_app = app
        #Retrieving datasource information
        if "poollist" in selected_app:
            for pool in selected_app['poollist']:
                for retrieved_ds in instance['datasource']:
                    if retrieved_ds['name'] == pool['name']:
                        convert_keys_names(retrieved_ds)  
                        pool['datasource'] = retrieved_ds
                        break
        else:
            logger.debug("No poollist key found for %s" % selected_app['name'])
            
        convert_keys_names(selected_app)        
        return render_to_response('platforms/oc4j/application.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL,"hostname":hostname, "instance_id":instance['id'] ,"application": selected_app}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/oc4j/application.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))


@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def get_app_list(request, filters, type):
    return HttpResponse(get_apps_list(request.user, filters, type))

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def get_instance_list(request, filters):
    servers = extract_servers(filters, request.user)
    instances = []
    for server in servers:
        instances.extend(extract_instances_name(server.hostname))
    return HttpResponse(json.dumps({"errors":"", "instances":instances}))
    
@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def get_deploy_form(request, dialog_name, action, filters):
    logger.debug('Rendering form')         
    return render_to_response('platforms/oc4j/deployform.html', {'action':action, 'filters':filters, 'form':DeployForm([]), 'dialog_name': dialog_name, 'base_url':settings.BASE_URL}, context_instance=RequestContext(request))

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def get_form(request, dialog_name, action, filters):
    logger.debug("Rendering %s form" % action)   
    if action == 'createinstance':   
        return render_to_response('platforms/oc4j/instanceform.html', {'action':action, 'filters':filters, 'form':InstanceForm([]), 'dialog_name': dialog_name, 'base_url':settings.BASE_URL}, context_instance=RequestContext(request))
    elif action == 'addpool':
        return render_to_response('platforms/oc4j/poolform.html', {'action':action, 'filters':filters, 'form':PoolForm([]), 'dialog_name': dialog_name, 'base_url':settings.BASE_URL}, context_instance=RequestContext(request))

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def deploy_app(request, filters, dialog_name, xhr=None):
    if request.method == "POST":
        logger.debug("Recreating form")
        form = DeployForm(request.POST)

        #Check if the <xhr> var had something passed to it.
        if xhr == "xhr":
            #TODO: Try to use dynamic form validation
            clean = form.is_valid()
            rdict = {'bad':'false', 'filters':filters }
            try:
                appfile = request.POST['applist']
                app_type = request.POST['types']
                instancename = request.POST['instancename']
                appname = request.POST['appname']
                action = request.POST['action']
            except:
                appname=None
                app_type=None
                action=None
            if appname and app_type and action:
                logger.debug("Parameters check: OK.")
                logger.debug("Calling MCollective to deploy %s application on %s filtered server" % (appfile, filters))
                response, content = callRestServer(request.user, filters, 'a7xoas', action, 'appname=%s;instancename=%s;appfile=%s' %(appname, instancename, appfile), True)
                if response.status == 200:
                    json_content = json.loads(content)
                    s_resps = []
                    for server_response in json_content:
                        if server_response['statuscode']==0:
                            s_resps.append({"server": server_response["sender"], "response":server_response["statusmsg"]})
                        else:
                            s_resps.append({"server": server_response["sender"], "message":server_response["statusmsg"]})
                    rdict.update({"result":s_resps})
                else:
                    rdict.update({"result": "KO", "message": "Error communicating with server"})
                
                rdict.update({'dialog_name':dialog_name})
                # And send it off.
            else:
                rdict.update({'bad':'true'})
                d = {}
                # This was painful, but I can't find a better way to extract the error messages:
                for e in form.errors.iteritems():
                    d.update({e[0]:unicode(e[1])}) # e[0] is the id, unicode(e[1]) is the error HTML.
                # Bung all that into the dict
                rdict.update({'errs': d })
                # Make a json whatsit to send back.
                
            return HttpResponse(json.dumps(rdict, ensure_ascii=False), mimetype='application/javascript')
        # It's a normal submit - non ajax.
        else:
            if form.is_valid():
                # We don't accept non-ajax requests for the moment
                return HttpResponseRedirect("/")
    else:
        # It's not post so make a new form
        logger.warn("Cannot access this page using GET")
        raise Http404
    
@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def get_log_form(request, dialog_name, action, filters):
    logger.debug('Rendering form')         
    return render_to_response('platforms/oc4j/logform.html', {'action':action, 'filters':filters, 'form':LogForm([]), 'dialog_name': dialog_name, 'base_url':settings.BASE_URL}, context_instance=RequestContext(request))


@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def get_log(request, filters, dialog_name, xhr=None):
    if request.method == "POST":
        logger.debug("Recreating form")
        form = LogForm(request.POST)

        #Check if the <xhr> var had something passed to it.
        if xhr == "xhr":
            #TODO: Try to use dynamic form validation
            clean = form.is_valid()
            rdict = {'bad':'false', 'filters':filters }
            try:
                instancename = request.POST['instancename']
                appname = request.POST['appname']
            except:
                instancename=None
                appname=None
            if instancename and appname:
                logger.debug("Parameters check: OK.")
                logger.debug("Calling MCollective to get log on %s filtered server" % (filters))
                response, content = callRestServer(request.user, filters, 'a7xoas', 'get_log', 'instancename=%s;appname=%s' % (instancename,appname), True)
                if response.status == 200:
                    json_content = json.loads(content)
                    s_resps = []
                    for server_response in json_content:
                        if server_response['statuscode']==0:
                            s_resps.append({"server": server_response["sender"], "logfile":server_response["data"]["logfile"]})
                        else:
                            s_resps.append({"server": server_response["sender"], "message":server_response["statusmsg"]})
                    rdict.update({"result":s_resps})
                else:
                    rdict.update({"result": "KO", "message": "Error communicating with server"})
                
                rdict.update({'dialog_name':dialog_name})
                # And send it off.
            else:
                rdict.update({'bad':'true'})
                d = {}
                # This was painful, but I can't find a better way to extract the error messages:
                for e in form.errors.iteritems():
                    d.update({e[0]:unicode(e[1])}) # e[0] is the id, unicode(e[1]) is the error HTML.
                # Bung all that into the dict
                rdict.update({'errs': d })
                # Make a json whatsit to send back.
                
            return HttpResponse(json.dumps(rdict, ensure_ascii=False), mimetype='application/javascript')
        # It's a normal submit - non ajax.
        else:
            if form.is_valid():
                # We don't accept non-ajax requests for the moment
                return HttpResponseRedirect("/")
    else:
        # It's not post so make a new form
        logger.warn("Cannot access this page using GET")
        raise Http404
    
@login_required()
def get_log_file(request, file_name):
    logger.debug('Get Log file %s' % file_name)         
    log_file_content = read_file_log(file_name)
    return HttpResponse(json.dumps({"logfilecontent":log_file_content}, ensure_ascii=False), mimetype='application/javascript')

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def create_instance(request, filters, dialog_name, xhr=None):
    if request.method == "POST":
        logger.debug("Recreating form")
        form = InstanceForm(request.POST)

        #Check if the <xhr> var had something passed to it.
        if xhr == "xhr":
            #TODO: Try to use dynamic form validation
            clean = form.is_valid()
            rdict = {'bad':'false', 'filters':filters }
            try:
                instancename = request.POST['instancename']
                groupname = request.POST['groupname']
                isflow = request.POST['isflow']
            except:
                instancename=None
                groupname=None
            if instancename and groupname:
                logger.debug("Parameters check: OK.")
                logger.debug("Calling MCollective to create instance %s on %s filtered server" % (instancename, filters))
                args = 'instancename=%s;groupname=%s' %(instancename, groupname)
                if isflow:
                    args = "%s;isflow=%s" % (args, isflow)
                response, content = callRestServer(request.user, filters, 'a7xoas', 'createinstance', args, True)
                if response.status == 200:
                    json_content = json.loads(content)
                    s_resps = []
                    for server_response in json_content:
                        if server_response['statuscode']==0:
                            response_message = 'Instance Created'
                            if server_response["statusmsg"] and server_response["statusmsg"]!='OK':
                                response_message = server_response["statusmsg"]
                            s_resps.append({"server": server_response["sender"], "response":response_message})
                        else:
                            s_resps.append({"server": server_response["sender"], "message":server_response["statusmsg"]})
                    rdict.update({"result":s_resps})
                else:
                    logger.error(str(content));
                    rdict.update({"result": "KO", "message": "Error communicating with server"})
                
                rdict.update({'dialog_name':dialog_name})
                # And send it off.
            else:
                rdict.update({'bad':'true'})
                d = {}
                # This was painful, but I can't find a better way to extract the error messages:
                for e in form.errors.iteritems():
                    d.update({e[0]:unicode(e[1])}) # e[0] is the id, unicode(e[1]) is the error HTML.
                # Bung all that into the dict
                rdict.update({'errs': d })
                # Make a json whatsit to send back.
                
            return HttpResponse(json.dumps(rdict, ensure_ascii=False), mimetype='application/javascript')
        # It's a normal submit - non ajax.
        else:
            if form.is_valid():
                # We don't accept non-ajax requests for the moment
                return HttpResponseRedirect("/")
    else:
        # It's not post so make a new form
        logger.warn("Cannot access this page using GET")
        raise Http404
    
@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def add_pool(request, filters, dialog_name, xhr=None):
    if request.method == "POST":
        logger.debug("Recreating form")
        form = PoolForm(request.POST)

        #Check if the <xhr> var had something passed to it.
        if xhr == "xhr":
            #TODO: Try to use dynamic form validation
            clean = form.is_valid()
            rdict = {'bad':'false', 'filters':filters }
            try:
                instancename = request.POST['instancename']
                poolname = request.POST['poolname']
                username = request.POST['username']
                password = request.POST['password']
                database = request.POST['database']
                dbinstance = request.POST['dbinstance']
            except:
                instancename=None
                poolname=None
                username=None
                password=None
                database=None
                dbinstance=None
                
            if instancename and poolname and username and password and database and dbinstance:
                logger.debug("Parameters check: OK.")
                logger.debug("Calling MCollective to create instance %s on %s filtered server" % (instancename, filters))
                response, content = callRestServer(request.user, filters, 'a7xoas', 'add_pool', 'oc4j=%s;poolname=%s;user=%s;password=%s;database=%s;instance=%s' %(instancename, poolname, username, password, database, dbinstance), True)
                if response.status == 200:
                    json_content = json.loads(content)
                    s_resps = []
                    for server_response in json_content:
                        if server_response['statuscode']==0:
                            s_resps.append({"server": server_response["sender"], "response":server_response["statusmsg"]})
                        else:
                            s_resps.append({"server": server_response["sender"], "message":server_response["statusmsg"]})
                    rdict.update({"result":s_resps})
                else:
                    rdict.update({"result": "KO", "message": "Error communicating with server"})
                
                rdict.update({'dialog_name':dialog_name})
                # And send it off.
            else:
                rdict.update({'bad':'true'})
                d = {}
                # This was painful, but I can't find a better way to extract the error messages:
                for e in form.errors.iteritems():
                    d.update({e[0]:unicode(e[1])}) # e[0] is the id, unicode(e[1]) is the error HTML.
                # Bung all that into the dict
                rdict.update({'errs': d })
                # Make a json whatsit to send back.
                
            return HttpResponse(json.dumps(rdict, ensure_ascii=False), mimetype='application/javascript')
        # It's a normal submit - non ajax.
        else:
            if form.is_valid():
                # We don't accept non-ajax requests for the moment
                return HttpResponseRedirect("/")
    else:
        # It's not post so make a new form
        logger.warn("Cannot access this page using GET")
        raise Http404