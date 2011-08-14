'''
Created on Aug 10, 2011

@author: mmornati
'''
import httplib2
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import json
import logging

logger = logging.getLogger(__name__)

def callRestServer(filters, agent, action, args=None):
    http = httplib2.Http()
    url = settings.RUBY_REST_BASE_URL
    url += filters + "/"
    url += agent + "/"
    url += action + "/"
    if args:
        url += args + "/"
    logger.info('Calling RestServer on: ' + url)
    response, content = http.request(url, "GET")
    logger.info('Response: ' + str(response))
    logger.info('Content: ' + str(content))
    return response, content

def get(request, filters, agent, action, args=None):
    response, content = callRestServer(filters, agent, action, args)
    if response.status == 200:
        return HttpResponse(content, mimetype="application/json")
    return response

def getWithTemplate(request, template, filters, agent, action, args=None):
    response, content = callRestServer(filters, agent, action, args)
    if response.status == 200:
        jsonObj = json.loads(content)
        templatePath = 'ajax/' + template + '.html'
        data = {
                'content': jsonObj
        }
        return render_to_response( templatePath, data,
            context_instance = RequestContext( request ) )
    return response

