'''
Created on Sep 9, 2011

@author: mmornati
'''
from django import forms
from webui.platforms.oc4j import settings

class DeployForm(forms.Form):
    types = forms.ChoiceField(choices=settings.AVAILABLE_TYPES, required=True)
    applist = forms.ChoiceField(label=u"Available application", required=True)
    instancename = forms.ChoiceField(label=u"Instance Name", required=True)
    appname = forms.CharField(label=u"Application Name", required=True)
    
class LogForm(forms.Form):
    instancename = forms.ChoiceField(label=u"Instance Name", required=True)
    appname = forms.CharField(label=u"Application Name", required=True)
    
class InstanceForm(forms.Form):
    instancename = forms.CharField(label=u"Instance Name", required=True)
    groupname = forms.CharField(label=u"Group Name", required=True)
    isflow = forms.CharField(label=u"Is Flow?", required=False)
    
class PoolForm(forms.Form):
    poolname = forms.CharField(label=u"Pool name", required=True)
    instancename = forms.CharField(label=u"Oc4J Name", required=True)
    username = forms.CharField(label=u"Database Username", required=True)
    password = forms.CharField(widget=forms.PasswordInput, label=u"Database Password", required=True)
    database = forms.CharField(label=u"Server Name", required=True)
    dbinstance = forms.CharField(label=u"Database Instance", required=True)
    