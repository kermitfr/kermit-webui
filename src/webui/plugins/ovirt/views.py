'''
Created on Nov 7, 2012

@author: mmornati
'''
import logging
from django.contrib.auth.decorators import login_required
from webui.core import generate_commons_page_dict
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from webui.servers.utils import get_server_operations
from django.http import HttpResponse
from django.utils import simplejson as json
from webui.restserver.communication import callRestServer

logger = logging.getLogger(__name__)

@login_required()
def create_vm(request, hostname):
    server_info = []   
    return render_to_response('plugins/ovirt/createvm.html', dict({"serverdetails": server_info, "hostname": hostname, 'server_operations': get_server_operations(request,hostname)}, **generate_commons_page_dict(request)), context_instance=RequestContext(request))

@login_required()
def get_clusters(request, hostname):
    logger.debug("Calling get_clusters")
    clusters_list = []
    filters = "identity=%s" % hostname
    response, content = callRestServer(request.user, filters, "ovirt", "get_clusters", wait_response=True, use_task=True)
    if response.getStatus() == 200 and len(content)>0:
        if len(content) > 1:
            logger.warn("More than one server sent a response.")
        if "clusters" in content[0].getData():
            for cluster in content[0].getData()["clusters"]:
                clusters_list.append({"id": cluster["id"], "name": cluster["name"]})
    return HttpResponse(json.dumps(clusters_list, ensure_ascii=False), mimetype='application/javascript')



@login_required()
def get_templates(request, hostname):
    logger.debug("Calling get_templates")
    templates_list = []
    filters = "identity=%s" % hostname
    response, content = callRestServer(request.user, filters, "ovirt", "get_templates", wait_response=True, use_task=True)
    if response.getStatus() == 200 and len(content)>0:
        if len(content) > 1:
            logger.warn("More than one server sent a response.")
        if "templates" in content[0].getData():
            for template in content[0].getData()["templates"]:
                templates_list.append({"id": template["id"], "name": template["name"]})
    return HttpResponse(json.dumps(templates_list, ensure_ascii=False), mimetype='application/javascript')
    