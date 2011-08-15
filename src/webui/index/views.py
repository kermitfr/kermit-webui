from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template import RequestContext
from webui.index.models import *
from webui.defaultop.models import Operation

def index(request):
    #if not request.user.is_authenticated():
    #    return HttpResponseRedirect(reverse('login'))
    #items = Menu.objects.filter(enabled=True).order_by('order')
    operations = Operation.objects.filter(enabled=True)
    return render_to_response('index/index.html', {"base_url": settings.BASE_URL, "operations": operations}, context_instance=RequestContext(request))


def credits(request):
    return render_to_response('index/credits.html', context_instance=RequestContext(request))
