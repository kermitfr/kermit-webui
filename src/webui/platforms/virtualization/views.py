'''
Created on Nov 3, 2011

@author: mmornati
'''
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from webui import settings
from django.template.context import RequestContext
import logging
from webui.restserver.communication import callRestServer
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from webui.serverstatus.models import Server

logger = logging.getLogger(__name__)

@login_required
def get_server_details(request, hostname, instance_name, resource_name):
    filter = "identity=%s"%hostname
    server = Server.objects.get(hostname=hostname)
    response, content = callRestServer(request.user, filter, "libvirt", "hvinfo", None, True)
    if response.getStatus() == 200:
        virtual = content[0]
        domains = []
        for dom in virtual.getData()['inactive_domains']:
            info = {'name': dom,
                    'active': False,
                    'start_url': reverse('call_mcollective_with_arguments', kwargs={'filters':filter, 'agent':"libvirt", 'action':"start", 'args':"domain=%s"%dom, 'wait_for_response':True}),
                    'stop_url': reverse('call_mcollective_with_arguments', kwargs={'filters':filter, 'agent':"libvirt", 'action':"shutdown", 'args':"domain=%s"%dom, 'wait_for_response':True})
                    }
            domains.append(info)
        for dom in virtual.getData()['active_domains']:
            vnc_agent = server.agents.filter(name='libvirtvnc')
            novnc_url = None
            if len(vnc_agent) > 0:
                novnc_url = '%s/novnc/vnc_auto.html?host=%s&port=6080' % (settings.STATIC_URL, hostname)
            info = {'name': dom,
                    'active': True,
                    'start_url': reverse('call_mcollective_with_arguments', kwargs={'filters':filter, 'agent':"libvirt", 'action':"start", 'args':"domain=%s"%dom, 'wait_for_response':False}),
                    'stop_url': reverse('call_mcollective_with_arguments', kwargs={'filters':filter, 'agent':"libvirt", 'action':"shutdown", 'args':"domain=%s"%dom, 'wait_for_response':False}),
                    'start_vnc_proxy_url': reverse('start_vnc_proxy', kwargs={'hostname':hostname, 'domain': dom}),
                    'novnc_url': novnc_url
                    }
            domains.append(info)
        return render_to_response('platforms/virtualization/server.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname, 'filter': filter ,'virtual': virtual.getData(), 'domains': domains}, context_instance=RequestContext(request))
    else:     
        return render_to_response('platforms/virtualization/server.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))
    
    
def start_vnc_proxy(request, hostname, domain):
    response, content = callRestServer(request.user, "identity=%s"%hostname, "libvirtvnc", "start_proxy", "domain=%s"%domain, True)
    if response.getStatus() == 200:
        json_data = []
        for entry in content:
            json_data.append(entry.to_dict())
        return HttpResponse(json_data, mimetype='application/javascript')
    else:
        print "ERRROR"
    