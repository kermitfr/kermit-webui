'''
Created on Aug 10, 2011

@author: mmornati
'''
import httplib2
from django.http import HttpResponse
from django.conf import settings

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

