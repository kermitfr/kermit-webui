'''
Created on Nov 15, 2012

@author: mmornati
'''
from django import forms
from webui.plugins.ovirt import settings


class CreateVMForm(forms.Form):
    name = forms.CharField(label=u"VirtualMachine Name", required=True)
    cluster = forms.ChoiceField(choices=settings.AVAILABLE_TYPES, required=True)
    template = forms.ChoiceField(choices=settings.AVAILABLE_TYPES, required=True)
    memory = forms.CharField(label=u"Memory", required=True)

class AddStorageForm(forms.Form):
    size = forms.CharField(label=u"Storage Size", required=True)
    type = forms.ChoiceField(choices=settings.AVAILABLE_TYPES, required=True)
    interface = forms.ChoiceField(choices=settings.AVAILABLE_TYPES, required=True)
    format = forms.ChoiceField(choices=settings.AVAILABLE_TYPES, required=True)
    bootable = forms.BooleanField(label=u"Is Bootable?", required=True)
    
class AddNetworkForm(forms.Form):
    name = forms.CharField(label=u"NIC Name", required=True)
    interface = forms.ChoiceField(choices=settings.AVAILABLE_TYPES, required=True)
    network_name = forms.CharField(label=u"Network Name", required=True)
