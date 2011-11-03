'''
Created on Nov 3, 2011

@author: mmornati
'''
from django.contrib.auth.decorators import login_required
from webui.platforms.jboss.communication import read_server_info
from django.shortcuts import render_to_response
from webui import settings
from django.template.context import RequestContext

@login_required
def jboss_details(request, hostname, instance_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        jboss_home = ""
        jboss_ver = ""
        java_ver = ""
        java_bin = ""
        server_name = ""
        if 'jboss_home' in server_info:
            jboss_home = server_info["jboss_home"]
        if 'jboss_ver' in server_info:
            jboss_ver = server_info["jboss_ver"]
        if 'java_ver' in server_info:
            java_ver = server_info["java_ver"]
        if 'java_bin' in server_info:
            java_bin = server_info["java_bin"]
        if 'server_name' in server_info:
            server_name = server_info["server_name"]
        return render_to_response('platforms/jboss/server.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "jboss_home":jboss_home, "jboss_ver":jboss_ver, "java_ver": java_ver, "java_bin": java_bin, "server_name":server_name, "hostname": hostname}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/jboss/server.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))

