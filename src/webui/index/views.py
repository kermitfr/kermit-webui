from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from webui.widgets.loading import registry

def index(request):
    #if not request.user.is_authenticated():
    #    return HttpResponseRedirect(reverse('login'))
    #items = Menu.objects.filter(enabled=True).order_by('order')
    widgets = registry.get_widgets_dashboard()    
    return render_to_response('index/index.html', {"base_url": settings.BASE_URL, "widgets": widgets}, context_instance=RequestContext(request))


def credits(request):
    return render_to_response('index/credits.html', context_instance=RequestContext(request))
