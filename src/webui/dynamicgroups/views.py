'''
Created on Jul 20, 2012

@author: mmornati
'''
from webui.dynamicgroups.models import DynaGroup
from guardian.shortcuts import get_objects_for_user
import logging
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

logger = logging.getLogger(__name__)

@login_required()
def get_dynamicgroup_tree(request):
    dynagroups = DynaGroup.objects.all()
    if not request.user.is_superuser:
        dynagroups = get_objects_for_user(request.user, 'use_agent', DynaGroup).filter(enabled=True)
    data = []
    for dynag in dynagroups:
        dbservers = dynag.servers
        servers = []
        for dbs in dbservers.iterator():
            if request.user.has_perm('use_server', dbs):
                servers.append(dbs)
        content = {"isFolder": "true", "title": dynag.name, "key":dynag.name}
        if len(servers) > 0:
            children = []
            for s in servers:
                action_data = {"title": s.hostname, "key":s.hostname, "group":dynag.name}
                children.append(action_data)
            content['children'] = children
            
        data.append(content)
         
    return HttpResponse(json.dumps(data))