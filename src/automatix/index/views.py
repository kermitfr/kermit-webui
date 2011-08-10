from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template import RequestContext
from automatix.index.models import *

def index(request):
    #if not request.user.is_authenticated():
    #    return HttpResponseRedirect(reverse('login'))
    items = Menu.objects.filter(enabled=True).order_by('order')
    return render_to_response('index/index.html', {'username': ("%s %s"%('Try', 'Me')), "base_url": settings.BASE_URL, "items": items}, context_instance=RequestContext(request))


def credits(request):
    return render_to_response('index/credits.html', context_instance=RequestContext(request))
