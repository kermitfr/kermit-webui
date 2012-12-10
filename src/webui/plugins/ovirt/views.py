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
from webui.plugins.ovirt.forms import CreateVMForm, AddStorageForm,\
    AddNetworkForm

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

def submit_vm(request, hostname):
    if request.POST:
        
        vm_form = CreateVMForm(request.POST)
        storage_form = AddStorageForm(request.POST)
        network_form = AddNetworkForm(request.POST)
        
        logger.debug(vm_form.is_valid())
        logger.debug(storage_form.is_valid())
        logger.debug(network_form.is_valid())
        
#        vm_name = request.POST["base-name"]
#        storage_format = request.POST['storage-format']
#        storage_bootable = request.POST['storage-bootable']
#        storage_type = request.POST['storage-type']
#        template_id = request.POST['base-template']
#        memory = request.POST['base-memory']
#        network_name = request.POST['network-name']
#        cluster_id = request.POST['base-cluster']
#        storage_size = request.POST['storage-size']
#        network_interface = request.POST['network-interface']
#        network_name = request.POST['network-network_name']
#        storage_interface = request.POST['storage-interface']
        
    return HttpResponse()
    
    