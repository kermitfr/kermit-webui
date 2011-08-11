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

def get(request, filters, agent, action, args=None):
    http = httplib2.Http()
    url = settings.RUBY_REST_BASE_URL
    url += filters + "/"
    url += agent + "/"
    url += action + "/"
    if args:
        url += args + "/"
    print url
    response, content = http.request(url, "GET")
    if response.status == 200:
        return HttpResponse(content, mimetype="application/json")
        
    return response

def getWithTemplate(request, template, filters, agent, action, args=None):
    if request.is_ajax():
        http = httplib2.Http()
        url = settings.RUBY_REST_BASE_URL
        url += filters + "/"
        url += agent + "/"
        url += action + "/"
        if args:
            url += args + "/"
            
        response, content = http.request(url, "GET")
        if response.status == 200:
            jsonObj = json.loads(content)
            templatePath = 'ajax/' + template + '.html'
            data = {
                    'content': jsonObj
            }
            return render_to_response( templatePath, data,
                context_instance = RequestContext( request ) )
    return response

def executeScript(request, language, script):
    print language
    print script
    return ""

