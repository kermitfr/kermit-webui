import logging
from webui import settings
from webui.serverstatus.models import Server
import os
import glob
from django.utils import simplejson as json

logger = logging.getLogger(__name__)

def convert_keys_names(dict):
    for key,value in dict.items():
        if key.__contains__('-'):
            dict[key.replace('-', '_')]=value
            dict.pop(key, value)


def read_file_info(hostname, prefix, suffix):
    if hostname:
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
        file_content = None
        if (len(filesFound)>0):
            if len(filesFound) > 1:
                logger.warn("More than one inventory files found! Using just the first one")
                logger.warn(filesFound)           
                filesFound.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            try:
                file_content = open(filesFound[0], 'r').read()
            except:
                logger.error('Cannot access inventory file!!')
            
            return json.loads(file_content)
    return None