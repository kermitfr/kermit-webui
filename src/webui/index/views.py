from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.template import RequestContext
from webui.widgets.loading import registry
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from webui.servicestatus import utils

@login_required()
def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    #items = Menu.objects.filter(enabled=True).order_by('order')
    service_status = None
    if 'webui.servicestatus' in settings.INSTALLED_APPS:
        service_status = utils.test_services()
    widgets = registry.get_widgets_dashboard(request.user)    
    return render_to_response('index/index.html', {"base_url": settings.BASE_URL, "widgets": widgets, "service_status":service_status, "static_url":settings.STATIC_URL, 'service_status_url':settings.RUBY_REST_PING_URL}, context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    response = redirect(settings.LOGIN_URL)
    return response
 
@login_required()
def credits(request):
    return render_to_response('index/credits.html', context_instance=RequestContext(request))
