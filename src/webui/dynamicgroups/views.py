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
from webui.dynamicgroups.forms import DynaGroupEditForm
from django.template.loader import render_to_string
from django.template.context import RequestContext
from webui.dynamicgroups import tasks
from webui.puppetclasses.views import check_context_operation_visibility_list

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
        classes = check_context_operation_visibility_list(servers)
        filtername = None
        for s in servers:
            if filtername:
                filtername = "%s;%s" % (filtername, s.hostname)
            else:
                filtername = s.hostname
                
        content = {"isFolder": "true", "title": dynag.name, "key":dynag.name, "filtername":filtername, "classes":classes}
        if len(servers) > 0:
            children = []
            for s in servers:
                classes = check_context_operation_visibility_list(servers)
                action_data = {"title": s.hostname, "key":s.hostname, "group":dynag.name, "filtername":s.hostname, "classes":classes}
                children.append(action_data)
            content['children'] = children
            
        data.append(content)
         
    return HttpResponse(json.dumps(data))


def get_dynamicgroup_form(request, dynagroup_id=None):
    if not dynagroup_id:
        logger.debug('Rendering empty form')
        form = DynaGroupEditForm()
        return HttpResponse(render_to_string('widgets/dynagroups/modalform.html', {'form':form}, context_instance=RequestContext(request)))
    else:
        return None
    
@login_required()
def post_dynagroup_mods(request, xhr=None):
    if request.method == "POST":
        form = DynaGroupEditForm(request.POST)
        if xhr == "xhr":
            rdict = {'bad':'false'}
            if form.is_valid():
                logger.debug("Parameters check: OK.")
                name = form.cleaned_data['name']
                engine = form.cleaned_data['engine']
                objname = form.cleaned_data['objname']
                rule = form.cleaned_data['rule']
                value = form.cleaned_data['value']
                update = form.cleaned_data['force_update']
                
                dynag = DynaGroup.objects.create(name=name, engine=engine, obj_name=objname, rule=rule, value=value)
                
                if update:
                    logger.debug("Forcing dynagroup update")
                    tasks.update_single_dyna(request.user, dynag)
            else: 
                rdict.update({'bad':'true'})
                d = {}
                for e in form.errors.iteritems():
                    d.update({e[0]:unicode(e[1])}) # e[0] is the id, unicode(e[1]) is the error HTML.
                rdict.update({'errs': d })

            rdict.update({'dialog_name':'course-form'})
            return HttpResponse(json.dumps(rdict, ensure_ascii=False), mimetype='application/javascript') 
        
    return HttpResponse('', mimetype='application/javascript')
