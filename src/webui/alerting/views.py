'''
Created on Nov 17, 2011

@author: mmornati
'''
from django.http import HttpResponse
from webui.alerting.utils import send_server_inventory_email
from django.contrib.auth.decorators import login_required

@login_required
def send_inventory_mail(request):
    response = send_server_inventory_email()
    return HttpResponse('')