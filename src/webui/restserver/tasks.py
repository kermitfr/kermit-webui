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
#TODO: refactor using HTTP lib url generation
def httpcall(filters, agent, action, args, use_task=True):
    http = httplib2.Http(timeout=20)
    url = settings.RUBY_REST_BASE_URL
    url += filters + "/"
    url += agent + "/"
    url += action + "/"
    if args:
        url += args
        logger.debug('Calling RestServer on: ' + url)
    if use_task:
        httpcall.update_state(state="PROGRESS", meta={"current": 50, "total": 100})
    response, content = http.request(url, "GET")
    logger.debug('Response: ' + str(response))
    logger.debug('Content: ' + str(content))
    if use_task:
        httpcall.update_state(state="COMPLETED", meta={"current": 100, "total": 100})
    return response, content, agent, action