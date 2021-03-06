from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.template import RequestContext
from webui.widgets.loading import registry
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from webui.core import generate_commons_page_dict

@login_required()
def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    #items = Menu.objects.filter(enabled=True).order_by('order')
    widgets = registry.get_widgets_dashboard(request.user)    
    return render_to_response('index/index.html', dict({"widgets": widgets}, **generate_commons_page_dict(request)), context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    response = redirect(settings.LOGIN_URL)
    return response
