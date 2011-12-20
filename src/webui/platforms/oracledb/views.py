'''
Created on Nov 3, 2011

@author: mmornati
'''
from webui.platforms.oracledb.communication import read_server_info
from django.shortcuts import render_to_response
from webui import settings
from django.template.context import RequestContext
import logging
from django.contrib.auth.decorators import login_required
from guardian.decorators import permission_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from webui.platforms.oracledb.forms import SqlExecuteForm, CloneDatabaseForm
from webui.restserver.communication import callRestServer
from django.utils import simplejson as json
from webui.platforms.oracledb.utils import sql_list, extract_instances_name,\
    extract_schema, extract_compatible_servers
from webui.platforms.utils import read_file_log, extract_servers
logger = logging.getLogger(__name__)

@login_required
def get_details(request, hostname, database_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        version = ""
        if "version" in server_info:
            version = server_info["version"]
        datadir = ""
        if "data_dir" in server_info:
            datadir = server_info["data_dir"]
        return render_to_response('platforms/oracledb/server.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "pg_version": version, "pg_datadir": datadir, "hostname": hostname}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/oracledb/server.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))

def get_instance_details(request, hostname, database_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        found_db = None
        for instance in server_info["instances"]:
            if instance["instance_name"] == database_name:
                found_db = instance
                break
                
        return render_to_response('platforms/oracledb/database.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "instance":found_db, "hostname": hostname}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/oracledb/database.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def get_sql_list(request, filters):
    return HttpResponse(sql_list(request.user, filters))
    
@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def get_execute_form(request, dialog_name, action, filters):
    logger.debug('Rendering form')         
    return render_to_response('platforms/oracledb/executeform.html', {'action':action, 'filters':filters, 'form':SqlExecuteForm([]), 'dialog_name': dialog_name, 'base_url':settings.BASE_URL}, context_instance=RequestContext(request))


@login_required()
def get_log_file(request, file_name):
    logger.debug('Get Log file %s' % file_name)         
    log_file_content = read_file_log(file_name)
    return HttpResponse(json.dumps({"logfilecontent":log_file_content}, ensure_ascii=False), mimetype='application/javascript')

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def execute_sql(request, filters, dialog_name, xhr=None):
    if request.method == "POST":
        logger.debug("Recreating form")
        form = SqlExecuteForm(request.POST)

        #Check if the <xhr> var had something passed to it.
        if xhr == "xhr":
            #TODO: Try to use dynamic form validation
            clean = form.is_valid()
            rdict = {'bad':'false', 'filters':filters }
            try:
                sql_script = request.POST['sqllist']
                dbname = request.POST['dbname']
            except:
                sql_script=None
                dbname=None
            if sql_script:
                logger.debug("Parameters check: OK.")
                logger.debug("Calling MCollective to deploy %s sql on %s filtered server" % (sql_script, filters))
                user_ip_address = request.META.get('REMOTE_ADDR') 
                #;user=%s;userip=%s
                response, content = callRestServer(request.user, filters, 'oracledb', 'execute_sql', 'sqlfile=%s;instancename=%s' % (sql_script, dbname), True)
                #TODO: Improve reading content data
                if response.status == 200:
                    json_content = json.loads(content)
                    s_resps = []
                    for server_response in json_content:
                        if "data" in server_response and "logfile" in server_response["data"]:
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
@permission_required('agent.call_mcollective', return_403=True)
def get_form(request, dialog_name, action, filters):
    logger.debug("Rendering %s form" % action)   
    if action == 'clonedatabase':   
        return render_to_response('platforms/oracledb/clonedbform.html', {'action':action, 'filters':filters, 'form':CloneDatabaseForm([]), 'dialog_name': dialog_name, 'base_url':settings.BASE_URL}, context_instance=RequestContext(request))

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
def get_schema_list(request, filters, instancename):
    servers = extract_servers(filters, request.user)
    schemas = []
    for server in servers:
        extracted = extract_schema(server.hostname, instancename)
        for ext in extracted:
            if not ext in schemas:
                schemas.append(ext)
    return HttpResponse(json.dumps({"errors":"", "schemas":schemas}))

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def get_target_list(request, filters, schema):
    servers = extract_compatible_servers(schema)
    return HttpResponse(json.dumps({"errors":"", "servers":servers}))

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def clone_db(request, filters, dialog_name, xhr=None):
    if request.method == "POST":
        logger.debug("Recreating form")
        form = CloneDatabaseForm(request.POST)

        #Check if the <xhr> var had something passed to it.
        if xhr == "xhr":
            #TODO: Try to use dynamic form validation
            clean = form.is_valid()
            rdict = {'bad':'false', 'filters':filters }
            try:
                instance = request.POST['instance']
                schema = request.POST['schema']
                target_server = request.POST['targetserver']
                target_instance = request.POST['targetinstance']
            except:
                instance=None
                schema=None
                target_server=None
                target_instance=None
            if instance and schema and target_server and target_instance:
                logger.debug("Parameters check: OK.")
                logger.debug("Calling MCollective to export %s from %s to %s" % (schema, instance, target_server))
                response, content = callRestServer(request.user, filters, 'oracledb', 'export_database', 'instancename=%s;schema=%s' %(instance, schema), True)
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