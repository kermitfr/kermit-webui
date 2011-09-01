from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.template import RequestContext
from webui.widgets.loading import registry
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout

@login_required(login_url='/accounts/login/')
def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    #items = Menu.objects.filter(enabled=True).order_by('order')
    widgets = registry.get_widgets_dashboard()    
    return render_to_response('index/index.html', {"base_url": settings.BASE_URL, "widgets": widgets}, context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    response = redirect('/accounts/login/')
    return response
 
@login_required(login_url='/accounts/login/')
def credits(request):
    return render_to_response('index/credits.html', context_instance=RequestContext(request))
