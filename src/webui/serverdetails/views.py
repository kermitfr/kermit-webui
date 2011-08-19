from django.http import HttpResponse
import logging
from webui import settings
from django.template.context import RequestContext
from django.shortcuts import render_to_response
import glob
import os
from webui.serverstatus.models import Server

logger = logging.getLogger(__name__)


def hostInventory(request, hostname):
    prefix = '*oasinventory-'
    suffix = '-compact.json'
    logger.info("Calling Inventory for " + hostname)
    toSearch = settings.AMQP_RECEIVER_FOLDER + '/' + prefix + hostname + suffix
    filesFound = glob.glob(toSearch)
    if (len(filesFound) == 0):
        server = Server.objects.filter(hostname=hostname)
        if server:
            fqdn = server[0].fqdn
            logger.info("No inventory files found. Trying with fqdn: " + fqdn)
            toSearch = settings.AMQP_RECEIVER_FOLDER + '/' + prefix + fqdn + suffix
            filesFound = glob.glob(toSearch)
        else:
            logger.error("No server found in database with hostname " + hostname)
    file = None
    if (len(filesFound)>0):
        if len(filesFound) > 1:
            logger.warn("More than one inventory files found! Using just the first one")
            logger.warn(filesFound)           
            filesFound.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        try:
            file = open(filesFound[0], 'r').read()
        except:
            logger.error('Cannot access inventory file!!')
        
    return render_to_response('server/details.html', {"base_url": settings.BASE_URL, "serverdetails": file}, context_instance=RequestContext(request))
