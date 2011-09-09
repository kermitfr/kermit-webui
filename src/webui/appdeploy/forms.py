'''
Created on Sep 9, 2011

@author: mmornati
'''
from django import forms
from webui.appdeploy import settings

class DeployForm(forms.Form):
    types = forms.ChoiceField(choices=settings.AVAILABLE_TYPES)
    applist = forms.ChoiceField()
    
    
        
