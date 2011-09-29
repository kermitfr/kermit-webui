from django.http import HttpResponse, HttpResponseRedirect, Http404
import logging
from webui.restserver.communication import callRestServer
from django.contrib.auth.decorators import login_required
from guardian.decorators import permission_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from webui.sqldeploy.forms import SqlDeployForm
from django.utils import simplejson as json
from webui import settings
from webui.sqldeploy.utils import get_sql_list as sql_list

logger = logging.getLogger(__name__)

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def get_sql_list(request, filters):
    return HttpResponse(sql_list(request.user, filters))
    
@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def get_deploy_form(request, dialog_name, action, filters):
    logger.debug('Rendering form')         
    return render_to_response('sqldeploy/deployform.html', {'action':action, 'filters':filters, 'form':SqlDeployForm([]), 'dialog_name': dialog_name, 'base_url':settings.BASE_URL}, context_instance=RequestContext(request))

@login_required()
@permission_required('agent.call_mcollective', return_403=True)
def redeploy_sql(request, filters, dialog_name, xhr=None):
    if request.method == "POST":
        logger.debug("Recreating form")
        form = SqlDeployForm(request.POST)

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
            if dbname and sql_script:
                logger.debug("Parameters check: OK.")
                logger.debug("Calling MCollective to deploy %s sql on %s filtered server" % (sql_script, filters))
                user_ip_address = request.META.get('REMOTE_ADDR') 
                response, content = callRestServer(request.user, filters, 'a7xdeploy', 'redeploysql', 'sqlscript=%s;dbname=%s;user=%s;userip=%s' % (sql_script, dbname, request.user, user_ip_address))
                #TODO: Improve reading content data
                if response.status == 200:
                    rdict.update({"result":"SQL Deployed"})
                else:
                    rdict.update({"result": "Error deploying SQL"})
                
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