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

logger = logging.getLogger(__name__)

@login_required()
def create_vm(request, hostname):
    server_info = []   
    #TODO: Make a refactor to remove base_url and statis_url from context
    return render_to_response('plugins/ovirt/createvm.html', dict({"serverdetails": server_info, "hostname": hostname, 'server_operations': get_server_operations(request,hostname)}, **generate_commons_page_dict(request)), context_instance=RequestContext(request))