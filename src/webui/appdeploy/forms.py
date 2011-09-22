'''
Created on Sep 9, 2011

@author: mmornati
'''
from django import forms
from webui.appdeploy import settings

APPS_SERVER = (('','-Select-'),
               ('oc4j','OC4J'), 
               ('weblogic','WebLogic'))

class DeployForm(forms.Form):
    types = forms.ChoiceField(choices=settings.AVAILABLE_TYPES)
    applist = forms.ChoiceField()
    servertype = forms.ChoiceField(choices=APPS_SERVER)
    instancename = forms.ChoiceField()
    
        
