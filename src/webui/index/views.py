from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.template import RequestContext
from webui.widgets.loading import registry
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from webui import core
from webui.abstracts import CoreService
from webui import settings as kermitsettings
from webui.utils import read_kermit_version

@login_required()
def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    #items = Menu.objects.filter(enabled=True).order_by('order')
    services = core.kermit_modules.extract(CoreService)
    service_status = []
    show_status_bar = request.user.is_superuser or kermitsettings.SHOW_STATUS_BAR 
    if services and show_status_bar:
        for service in services:
            data = {"name": service.get_name(),
                    "description" : service.get_description(),
                    "status": service.get_status()}
            service_status.append(data)
    widgets = registry.get_widgets_dashboard(request.user)    
    version = read_kermit_version()
    return render_to_response('index/index.html', {"settings": kermitsettings, "base_url": settings.BASE_URL, "widgets": widgets, "service_status":service_status, "static_url":settings.STATIC_URL, "kermit_version":version}, context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    response = redirect(settings.LOGIN_URL)
    return response
 
@login_required()
def credits(request):
    return render_to_response('index/credits.html', context_instance=RequestContext(request))
