# Create your views here.
from webui.platforms.bar.communication import read_server_info
from django.contrib.auth.decorators import login_required
from webui.platforms.utils import convert_keys_names
from django.shortcuts import render_to_response
from webui import settings
from django.template.context import RequestContext
import logging
from guardian.decorators import permission_required
from webui.platforms.bar.forms import DeployForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from webui.platforms.bar.utils import get_available_bars
from webui.restserver.communication import callRestServer
from django.utils import simplejson as json

logger = logging.getLogger(__name__)

@login_required()
def poolInventory(request, hostname, console_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        selected_console = None 
        for console in server_info:
            if console['consolename'] == console_name:
                selected_console = console
                break 
        resource_name = resource_name.replace('_', '/')
        pool = None
        for current in selected_console['poollist']:
            if current['poolname'] == resource_name:
                pool = current
                convert_keys_names(pool)
                break
        return render_to_response('platforms/bar/datasource.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "datasource": pool}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/bar/datasource.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))

@login_required()
def poolsInventory(request, hostname, console_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        selected_console = None 
        for console in server_info:
            if console['consolename'] == console_name:
                selected_console = console
                break 
        resource_name = resource_name.replace('_', '/')
        return render_to_response('platforms/bar/datasources.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "datasources": selected_console['poollist']}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/bar/datasources.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))


@login_required()
def barInventory(request, hostname, console_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        selected_console = None 
        for console in server_info:
            if console['consolename'] == console_name:
                selected_console = console
                break 
        selected_bar = None 
        for bar in selected_console['barlist']:
            if bar['name'] == resource_name:
                selected_bar = bar
                break
        #Retrieving datasource information
        if "resources" in selected_bar:
            pool_info = []
            for pool in selected_bar['resources']:
                for retrieved_ds in selected_console['poollist']:
                    if retrieved_ds['poolname'] == pool:
                        convert_keys_names(retrieved_ds)  
                        pool_info.append(retrieved_ds)
                        break
            selected_bar['datasources'] = pool_info    
        else:
            logger.debug("No poollist key found for %s" % console['consolename'])
            
        convert_keys_names(selected_bar)        
        return render_to_response('platforms/bar/batch.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL,"hostname":hostname, "bar":selected_bar}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/bar/batch.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))


@login_required()
def barConsoleInventory(request, hostname, console_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        selected_console = None 
        for console in server_info:
            if console['consolename'] == console_name:
                selected_console = console
                break 
        
        if 'java_ver' in selected_console:
            java_version = selected_console["java_ver"]
        else:
            java_version = ""
              
        return render_to_response('platforms/bar/console.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL,"hostname":hostname, "java_version":java_version}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/bar/console.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))


@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def get_deploy_form(request, dialog_name, action, filters):
    logger.debug('Rendering form')         
    return render_to_response('platforms/bar/deployform.html', {'action':action, 'filters':filters, 'form':DeployForm([]), 'dialog_name': dialog_name, 'base_url':settings.BASE_URL}, context_instance=RequestContext(request))

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def get_bar_list(request, filters):
    return HttpResponse(get_available_bars(request.user, filters))

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def deploy_bar(request, filters, dialog_name, xhr=None):
    if request.method == "POST":
        logger.debug("Recreating form")
        form = DeployForm(request.POST)

        #Check if the <xhr> var had something passed to it.
        if xhr == "xhr":
            #TODO: Try to use dynamic form validation
            clean = form.is_valid()
            rdict = {'bad':'false', 'filters':filters }
            try:
                bcname = request.POST['bcname']
                barname = request.POST['barname']
            except:
                bcname=None
                barname=None
            if bcname and barname:
                logger.debug("Parameters check: OK.")
                logger.debug("Calling MCollective to deploy %s application on %s filtered server" % (barname, filters))
                response, content = callRestServer(request.user, filters, 'a7xbar', 'deploy', 'bcname=%s;filename=%s' %(bcname, barname), True)
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
    