'''
Created on Nov 3, 2011

@author: mmornati
'''
from webui.platforms.postgresql.communication import read_server_info
from django.shortcuts import render_to_response
from webui import settings
from django.template.context import RequestContext
import logging
from django.contrib.auth.decorators import login_required
from guardian.decorators import permission_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from webui.platforms.postgresql.forms import SqlExecuteForm
from webui.restserver.communication import callRestServer
from django.utils import simplejson as json
from webui.platforms.postgresql.utils import sql_list
from webui.platforms.utils import read_file_log
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
        return render_to_response('platforms/postgresql/server.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "pg_version": version, "pg_datadir": datadir, "hostname": hostname}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/postgresql/server.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))

def get_db_details(request, hostname, database_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        found_db = None
        for database in server_info["databases"]:
            if database["name"] == database_name:
                found_db = database
                break
                
        size = ""
        if found_db and "size" in found_db:
            size = found_db["size"]
        return render_to_response('platforms/postgresql/database.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "db_size":size, "db_name":database_name, "hostname": hostname}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/postgresql/database.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def get_sql_list(request, filters):
    return HttpResponse(sql_list(request.user, filters))
    
@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def get_execute_form(request, dialog_name, action, filters):
    logger.debug('Rendering form')         
    return render_to_response('platforms/postgresql/executeform.html', {'action':action, 'filters':filters, 'form':SqlExecuteForm([]), 'dialog_name': dialog_name, 'base_url':settings.BASE_URL}, context_instance=RequestContext(request))


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
                response, content = callRestServer(request.user, filters, 'postgresql', 'execute_sql', 'sqlfile=%s;dbname=%s' % (sql_script, dbname), True)
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