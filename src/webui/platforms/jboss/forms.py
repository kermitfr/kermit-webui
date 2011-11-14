'''
Created on Sep 9, 2011

@author: mmornati
'''
from django import forms
from webui.platforms.jboss import settings


class DeployForm(forms.Form):
    types = forms.ChoiceField(choices=settings.AVAILABLE_TYPES)
    applist = forms.ChoiceField(label=u"Available application")
    instancename = forms.ChoiceField(label=u"Instance Name")
    
class LogForm(forms.Form):
    instancename = forms.ChoiceField(label=u"Instance Name")