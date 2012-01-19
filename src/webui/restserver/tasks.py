'''
Created on Nov 23, 2011

@author: mmornati
'''
from celery.decorators import task
import logging
import httplib2
from webui import settings
import socket
from django.utils import simplejson as json
import time

logger = logging.getLogger(__name__)

@task()
#TODO: refactor using HTTP lib url generation
def httpcall(filters, agent, action, args, use_task=True):
    http = httplib2.Http(timeout=settings.RUBY_REST_SERVER_TIMEOUT)
    url = settings.RUBY_REST_BASE_URL
    url += filters + "/"
    url += agent + "/"
    url += action + "/"
    if args:
        url += args
        logger.debug('Calling RestServer on: ' + url)
    if use_task:
        httpcall.update_state(state="PROGRESS", meta={"current": 50, "total": 100})
    try:
        response, content = http.request(url, "GET")
    except socket.timeout:
        logger.error("Timeout exception")
        content = "Request Timeout"
        response = httplib2.Response( {
                            "content-type": "text/plain",
                            "status": "408",
                            "content-length": len(content)
                            })
        content = [{"data":{},"statuscode":1,"sender":filters,"statusmsg":"Connection Timeout!"}]
        return response, content, agent, action
    logger.debug('Response: ' + str(response))
    logger.debug('Content: ' + str(content))
    if use_task:
        httpcall.update_state(state="COMPLETED", meta={"current": 100, "total": 100})
    return response, content, agent, action

@task()
def httpcallscheduler(filters, agent, action, args, use_task=True):
    #/schedule/in/0s/no-filter/rpcutil/ping/
    http = httplib2.Http(timeout=settings.RUBY_REST_SERVER_TIMEOUT)
    url = settings.RUBY_REST_SCHEDULER_URL + "in/0s/"
    url += filters + "/"
    url += agent + "/"
    url += action + "/"
    if args:
        url += args
        logger.debug('Calling RestServer on: ' + url)
    if use_task:
        httpcall.update_state(state="PROGRESS", meta={"current": 50, "total": 100})
    try:
        response, content = http.request(url, "GET")
    except socket.timeout:
        logger.error("Timeout exception")
        content = "Request Timeout"
        response = httplib2.Response( {
                            "content-type": "text/plain",
                            "status": "408",
                            "content-length": len(content)
                            })
        content = [{"data":{},"statuscode":1,"sender":filters,"statusmsg":"Connection Timeout!"}]
        return response, content, agent, action
    
    if response.status == 200:
        json_content = json.loads(content)
        jobid = json_content[0]["data"]["jobid"]
        logger.debug('Job scheduled on backend with id: %s' % jobid)
        finished = False
        status_url = settings.RUBY_REST_SCHEDULER_STATUS_URL + jobid
        while not finished:
            time.sleep(10)
            logger.debug("Calling status url %s" % status_url)
            status_response, status_content = http.request(status_url, "GET")
            if status_response.status == 200:
                json_content_status = json.loads(status_content)
                finished = True
                for status_response in json_content_status:
                    if status_response["data"]["state"] != 'finished':
                        finished = False
                        break
                if finished:
                    logger.debug('Job finished')
                    finished = True
                    output_url = settings.RUBY_REST_SCHEDULER_STATUS_URL + jobid
                    output_response, output_content = http.request(output_url, "GET")
                    return output_response, output_content, agent, action
    
    logger.debug('Response: ' + str(response))
    logger.debug('Content: ' + str(content))
    if use_task:
        httpcall.update_state(state="COMPLETED", meta={"current": 100, "total": 100})
    return response, content, agent, action