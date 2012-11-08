'''
Created on Nov 23, 2011

@author: mmornati
'''
from celery.task import task
import logging
import httplib2
from webui import settings
import socket
from django.utils import simplejson as json
import time
from webui.restserver.utils import convert_parameters_to_hash, convert_filters_to_hash

logger = logging.getLogger(__name__)

@task()
def httpcall(filters, agent, action, args, use_task=True, limit=None):
    #Fix for javascript "null" value
    if filters and filters=='null':
        filters = None
    http = httplib2.Http(timeout=settings.RUBY_REST_SERVER_TIMEOUT)
    url = "%s%s/%s/" % (settings.RUBY_REST_BASE_URL, agent, action)
    dictionary = {
        "filters": convert_filters_to_hash(filters)
    }
    if limit:
        dictionary["limit"] = {"targets": limit, "method":"random"}
    if args:
        dictionary["parameters"] = convert_parameters_to_hash(args)
        logger.debug('Calling RestServer on: ' + url)
    if use_task:
        httpcall.update_state(state="PROGRESS", meta={"current": 50, "total": 100})
    try:
        response, content = http.request(url, "POST", headers={'Content-Type': 'application/json; charset=UTF-8'}, body=json.dumps(dictionary),)
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
def httpcallscheduler(filters, agent, action, args, use_task=True, limit=None):
    #Fix for javascript "null" value
    if filters and filters=='null':
        filters = None
    http = httplib2.Http(timeout=settings.RUBY_REST_SERVER_TIMEOUT)
    url = "%s%s/%s/" % (settings.RUBY_REST_BASE_URL, agent, action)
    dictionary = {
        "filters": convert_filters_to_hash(filters),
        "schedule": {
             "schedtype": "in",
             "schedarg": "0s"
        }
    }
    
    if limit:
        dictionary["limit"] = {"targets": limit, "method":"random"}
    if args:
        dictionary["parameters"] = convert_parameters_to_hash(args)
        logger.debug('Calling RestServer on: ' + url)
    if use_task:
        httpcallscheduler.update_state(state="PROGRESS", meta={"current": 50, "total": 100})
    try:
        response, content = http.request(url, "POST", headers={'Content-Type': 'application/json; charset=UTF-8'}, body=json.dumps(dictionary),)
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
        status_url = settings.RUBY_REST_SCHEDULER_STATUS_URL + jobid + '/'
        status_dict = {
            "filters": convert_filters_to_hash(filters)
        }
        while not finished:
            logger.debug("Calling status url %s" % status_url)
            status_response, status_content = http.request(status_url, "POST", headers={'Content-Type': 'application/json; charset=UTF-8'}, body=json.dumps(status_dict),)
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
                    output_url = settings.RUBY_REST_SCHEDULER_OUTPUT_URL + jobid + '/'
                    output_response, output_content = http.request(output_url, "POST", headers={'Content-Type': 'application/json; charset=UTF-8'}, body=json.dumps(dictionary),)
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
