'''
Created on Nov 23, 2011

@author: mmornati
'''
from celery.decorators import task
import logging
import httplib2
from webui import settings

logger = logging.getLogger(__name__)

@task()
def httpcall(filters, agent, action, args):
    http = httplib2.Http(timeout=20)
    url = settings.RUBY_REST_BASE_URL
    url += filters + "/"
    url += agent + "/"
    url += action + "/"
    if args:
        url += args
        logger.debug('Calling RestServer on: ' + url)
    response, content = http.request(url, "GET")
    logger.debug('Response: ' + str(response))
    logger.debug('Content: ' + str(content))
    return response, content