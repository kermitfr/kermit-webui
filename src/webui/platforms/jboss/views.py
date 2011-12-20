'''
Created on Nov 3, 2011

@author: mmornati
'''
from django.contrib.auth.decorators import login_required
from webui.platforms.jboss.communication import read_server_info
from django.shortcuts import render_to_response
from webui import settings
from django.template.context import RequestContext
import logging
from guardian.decorators import permission_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from webui.restserver.communication import callRestServer
from django.utils import simplejson as json
from webui.platforms.utils import extract_servers, read_file_log
from webui.platforms.jboss.utils import extract_instances_name, get_apps_list
from webui.platforms.jboss.forms import DeployForm, LogForm

logger = logging.getLogger(__name__)

@login_required
def jboss_details(request, hostname, instance_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        jboss_home = ""
        jboss_ver = ""
        java_ver = ""
        java_bin = ""
        server_name = ""
        if 'jboss_home' in server_info:
            jboss_home = server_info["jboss_home"]
        if 'jboss_ver' in server_info:
            jboss_ver = server_info["jboss_ver"]
        if 'java_ver' in server_info:
            java_ver = server_info["java_ver"]
        if 'java_bin' in server_info:
            java_bin = server_info["java_bin"]
        if 'server_name' in server_info:
            server_name = server_info["server_name"]
        return render_to_response('platforms/jboss/server.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "jboss_home":jboss_home, "jboss_ver":jboss_ver, "java_ver": java_ver, "java_bin": java_bin, "server_name":server_name, "hostname": hostname}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/jboss/server.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))

def jboss_app_details(request, hostname, instance_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        application = None
        for instance in server_info["instances"]:
            if instance["name"] == instance_name:
                for appli in instance['applilist']:
                    if appli["name"] == resource_name:
                        application = appli
                        break
                break
        
        return render_to_response('platforms/jboss/application.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "application":application, "hostname": hostname}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/jboss/application.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))

def jboss_ds_details(request, hostname, instance_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        datasource = None
        for instance in server_info["instances"]:
            if instance["name"] == instance_name:
                for datasource in instance['datasources']:
                    if datasource["jndi_name"] == resource_name:
                        datasource = datasource
                        break
                break
        
        return render_to_response('platforms/jboss/datasource.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "datasource":datasource, "hostname": hostname}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/jboss/datasource.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))


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
    return render_to_response('platforms/jboss/deployform.html', {'action':action, 'filters':filters, 'form':DeployForm([]), 'dialog_name': dialog_name, 'base_url':settings.BASE_URL}, context_instance=RequestContext(request))

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def redeploy_app(request, filters, dialog_name, xhr=None):
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
            except:
                app_type=None
            if app_type and instancename and appfile:
                logger.debug("Parameters check: OK.")
                logger.debug("Calling MCollective to deploy %s application on %s filtered server" % (appfile, filters))
                response, content = callRestServer(request.user, filters, 'jboss', 'deploy', 'appfile=%s;instancename=%s' % (appfile,instancename), True)
                if response.status == 200:
                    json_content = json.loads(content)
                    s_resps = []
                    for server_response in json_content:
                        if server_response['statuscode']==0:
                            s_resps.append({"server": server_response["sender"], "response":server_response["data"]["status"]})
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
    return render_to_response('platforms/jboss/logform.html', {'action':action, 'filters':filters, 'form':LogForm([]), 'dialog_name': dialog_name, 'base_url':settings.BASE_URL}, context_instance=RequestContext(request))


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
            except:
                instancename=None
            if instancename:
                logger.debug("Parameters check: OK.")
                logger.debug("Calling MCollective to get log on %s filtered server" % (filters))
                response, content = callRestServer(request.user, filters, 'jboss', 'get_log', 'instancename=%s' % (instancename), True)
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