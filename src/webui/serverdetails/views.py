from django.http import HttpResponse
import logging
from webui import settings
from django.template.context import RequestContext
from django.shortcuts import render_to_response
import glob
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)


def hostInventory(request, hostname):
    prefix = '*oasinventory-'
    suffix = '-pretty.json'
    logger.info("Calling Inventory for " + hostname)
    toSearch = settings.AMQP_RECEIVER_FOLDER + '/' + prefix + hostname + suffix
    filesFound = glob.glob(toSearch)
    if not len(filesFound) == 1:
        logger.warn("More than one inventory files found! Using just the first one")
        logger.warn(filesFound)           
    file = None
    try:
        file = open(filesFound[0], 'r').read()
    except:
        logger.error('Cannot access inventory file!!')
        
    return render_to_response('server/details.html', {"base_url": settings.BASE_URL, "serverdetails": file}, context_instance=RequestContext(request))
