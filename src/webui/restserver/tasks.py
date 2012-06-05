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
        httpcallscheduler.update_state(state="PROGRESS", meta={"current": 50, "total": 100})
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
        if len(json_content)==0:
            logger.warn("No response received!!")
            return response, content, agent, action
        
        logger.debug("Looking for jobid in response")
        jobid = None
        for data_received in json_content:
            #if "data" in data_received and "jobid" in data_received["data"]:
            if data_received and "data" in data_received and data_received["data"] and "jobid" in data_received["data"]:
                jobid = data_received["data"]["jobid"]
                break
                
        if not jobid:
            logger.warn("JobID not found in response data")
            response = httplib2.Response( {
                            "content-type": "text/plain",
                            "status": "200",
                            "content-length": len(content)
                            })
            content = json.dumps([{"data":{},"statuscode":0,"sender":filters,"statusmsg":"No response received! Check if Backend Scheduler is started"}])
            return response, content, agent, action
        
        logger.debug('Job scheduled on backend with id: %s' % jobid)
        finished = False
        status_url = settings.RUBY_REST_SCHEDULER_STATUS_URL + jobid + '/' + filters
        while not finished:
            logger.debug("Calling status url %s" % status_url)
            status_response, status_content = http.request(status_url, "GET")
            if status_response.status == 200:
                json_content_status = json.loads(status_content)
                finished = True
                for status_response in json_content_status:
                    #if "data" in status_response and "state" in status_response["data"]:
                    if status_response and "data" in status_response and status_response["data"] and "state" in status_response["data"]:
                        if status_response["data"]["state"] != 'finished' and status_response["data"]["state"] != 'lost in space':
                            finished = False
                            break
                if finished:
                    logger.debug('Job finished')
                    finished = True
                    output_url = settings.RUBY_REST_SCHEDULER_OUTPUT_URL + jobid + '/' + filters
                    output_response, output_content = http.request(output_url, "GET")
                    logger.debug('Response: ' + str(output_response))
                    logger.debug('Content: ' + str(output_content))
                    return output_response, output_content, agent, action
                else:
                    time.sleep(10)
    
    logger.debug('Response: ' + str(response))
    logger.debug('Content: ' + str(content))
    if use_task:
        httpcallscheduler.update_state(state="COMPLETED", meta={"current": 100, "total": 100})
    return response, content, agent, action
