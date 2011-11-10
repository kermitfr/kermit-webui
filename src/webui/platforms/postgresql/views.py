'''
Created on Nov 3, 2011

@author: mmornati
'''
from django.contrib.auth.decorators import login_required
from webui.platforms.postgresql.communication import read_server_info
from django.shortcuts import render_to_response
from webui import settings
from django.template.context import RequestContext
import logging

logger = logging.getLogger(__name__)

@login_required
def get_details(request, hostname, database_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        version = ""
        if "version" in server_info:
            version = server_info["version"]
        datadir = ""
        if "data_dir" in server_info:
            datadir = server_info["data_dir"]
        return render_to_response('platforms/postgresql/server.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "pg_version": version, "pg_datadir": datadir, "hostname": hostname}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/postgresql/server.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))

def get_db_details(request, hostname, database_name, resource_name):
    server_info = read_server_info(hostname)
    if server_info:
        found_db = None
        for database in server_info["databases"]:
            if database["name"] == database_name:
                found_db = database
                break
                
        size = ""
        if found_db and "size" in found_db:
            size = found_db["size"]
        return render_to_response('platforms/postgresql/database.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "db_size":size, "db_name":database_name, "hostname": hostname}, context_instance=RequestContext(request))
    else:
        return render_to_response('platforms/postgresql/database.html', {"base_url": settings.BASE_URL, "static_url":settings.STATIC_URL, "hostname": hostname}, context_instance=RequestContext(request))
