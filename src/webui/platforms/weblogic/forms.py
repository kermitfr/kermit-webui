'''
Created on Sep 9, 2011

@author: mmornati
'''
from django import forms
from webui.platforms.weblogic import settings

class DeployForm(forms.Form):
    types = forms.ChoiceField(choices=settings.AVAILABLE_TYPES, required=True)
    applist = forms.ChoiceField(label=u"Available application", required=True)
    instancename = forms.ChoiceField(label=u"Instance Name", required=True)
    appname = forms.CharField(label=u"Application Name", required=True)
    
class LogForm(forms.Form):
    instancename = forms.ChoiceField(label=u"Instance Name", required=True)
    
class InstanceForm(forms.Form):
    instancename = forms.CharField(label=u"Instance Name", required=True)
