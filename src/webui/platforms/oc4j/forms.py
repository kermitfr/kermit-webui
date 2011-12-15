'''
Created on Sep 9, 2011

@author: mmornati
'''
from django import forms
from webui.platforms.oc4j import settings

class DeployForm(forms.Form):
    types = forms.ChoiceField(choices=settings.AVAILABLE_TYPES)
    applist = forms.ChoiceField(label=u"Available application")
    instancename = forms.ChoiceField(label=u"Instance Name")
    appname = forms.CharField(label=u"Application Name")
    
class LogForm(forms.Form):
    instancename = forms.ChoiceField(label=u"Instance Name")
    appname = forms.CharField(label=u"Application Name")
    
class InstanceForm(forms.Form):
    instancename = forms.CharField(label=u"Instance Name", required=True)
    groupname = forms.CharField(label=u"Group Name", required=True)
    isflow = forms.CharField(label=u"Is Flow?", required=False)
    
class PoolForm(forms.Form):
    poolname = forms.CharField(label=u"Pool name")
    instancename = forms.CharField(label=u"Instance Name")
    username = forms.CharField(label=u"Database Username")
    password = forms.CharField(widget=forms.PasswordInput, label=u"Database Password")
    database = forms.CharField(label=u"Database connection")
    dbinstance = forms.CharField(label=u"Database Instance")
    