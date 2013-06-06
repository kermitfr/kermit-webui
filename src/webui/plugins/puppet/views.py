'''
Created on Nov 7, 2012

@author: mmornati
'''
import logging
from django.contrib.auth.decorators import login_required
from webui.abstracts import ServerOperation
from webui.puppetclasses.models import PuppetClass
import redis
from webui import settings, core
from webui.core import generate_commons_page_dict
from webui.servers.models import Server
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from webui.restserver.communication import callRestServer
from django.http import HttpResponse
from django.utils import simplejson as json
from webui.servers.utils import get_server_operations


logger = logging.getLogger(__name__)
@login_required()
def server_edit(request, hostname):
    server_info = []   
    return render_to_response('server/edit.html', dict({"serverdetails": server_info, "hostname": hostname, 'server_operations': get_server_operations(request,hostname)}, **generate_commons_page_dict(request)), context_instance=RequestContext(request))

@login_required()
def submit_server_edit(request, hostname):
    if (request.POST and "values" in request.POST):
        server_classes = request.POST.getlist('values')
        try:
            server = Server.objects.get(hostname=hostname)
        except:
            logger.debug("Trying to get server using fqdn")
            server = Server.objects.get(fqdn=hostname)
        try:
            redis_server = redis.Redis(host="%s"%settings.HIERA_REDIS_SERVER, password="%s"%settings.HIERA_REDIS_PASSWORD, port=settings.HIERA_REDIS_PORT, db=settings.HIERA_REDIS_DB)

            current_server_classes = redis_server.smembers("%s:%s" % (hostname, "classes"))
            for current_class in server_classes:
                retrieved = PuppetClass.objects.filter(name=current_class)
                if not current_class in current_server_classes and not retrieved[0] in server.puppet_classes.all():
                    redis_server.sadd("%s:%s" % (hostname, "classes"), current_class)
                    if retrieved:     
                        server.puppet_classes.add(retrieved[0])
            
            for current_class in current_server_classes:
                if not current_class in server_classes:
                    redis_server.srem("%s:%s" % (hostname, "classes"), current_class)
                    retrieved = PuppetClass.objects.filter(name=current_class)
                    if retrieved:     
                        server.puppet_classes.remove(retrieved[0])
            logger.debug("New server classes in the Hiera Redis Database: %s" % redis_server.smembers("%s:%s" % (hostname, "classes")))
            
            if "forceUpdate" in request.POST and request.POST["forceUpdate"] == "true":
                logger.info("Calling puppet force update for modified server %s" % hostname)
                filters = "identity=%s" % hostname
                response, content = callRestServer(request.user, filters, "puppet", "runonce", None, wait_response=True, use_task=False)
                if response.getStatus() == 200:
                    for msg in content:
                        if msg.getStatusMessage() == 'OK':
                            logger.info("Server correctly updated");
                            #TODO: Send this information back to user
                
        except:
            return HttpResponse(json.dumps({"result": "KO"}, ensure_ascii=False), mimetype='application/javascript')
    return HttpResponse(json.dumps({"result": "OK"}, ensure_ascii=False), mimetype='application/javascript')
