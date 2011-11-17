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
import simplejson as json
from django.core.urlresolvers import reverse

logger = logging.getLogger(__name__)

@login_required
def get_server_details(request, hostname, instance_name, resource_name):
    filter = "identity_filter=%s"%hostname
    response, content = callRestServer(request.user, filter, "libvirt", "hvinfo")
    if response.status == 200:
        virtual = json.loads(content)[0]
        domains = []
        for dom in virtual['data']['inactive_domains']:
            info = {'name': dom,
                    'active': False,
                    'start_url': reverse('call_mcollective_with_arguments', kwargs={'filters':filter, 'agent':"libvirt", 'action':"start", 'args':"domain=%s"%dom}),
                    'stop_url': reverse('call_mcollective_with_arguments', kwargs={'filters':filter, 'agent':"libvirt", 'action':"shutdown", 'args':"domain=%s"%dom})
                    }
            domains.append(info)
        for dom in virtual['data']['active_domains']:
            info = {'name': dom,
                    'active': True,
                    'start_url': reverse('call_mcollective_with_arguments', kwargs={'filters':filter, 'agent':"libvirt", 'action':"start", 'args':"domain=%s"%dom}),
                    'stop_url': reverse('call_mcollective_with_arguments', kwargs={'filters':filter, 'agent':"libvirt", 'action':"shutdown", 'args':"domain=%s"%dom})
                    }
            domains.append(info)
        return render_to_response('platforms/virtualization/server.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname, 'filter': filter ,'virtual': virtual['data'], 'domains': domains}, context_instance=RequestContext(request))
    else:     
        return render_to_response('platforms/virtualization/server.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))
    