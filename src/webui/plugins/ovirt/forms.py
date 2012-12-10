'''
Created on Nov 15, 2012

@author: mmornati
'''
from django import forms
from webui.plugins.ovirt import settings
from webui import core


class CreateVMForm(forms.Form):
    name = forms.CharField(label=u"VirtualMachine Name", required=True)
    cluster = core.KermitDynamicChoiceField(required=True)
    template = core.KermitDynamicChoiceField(required=True)
    memory = forms.CharField(label=u"Memory", required=True)

class AddStorageForm(forms.Form):
    size = forms.CharField(label=u"Storage Size", required=True)
    type = forms.ChoiceField(choices=settings.STORAGE_TYPES, required=True)
    interface = forms.ChoiceField(choices=settings.STORAGE_INTERFACE, required=True)
    format = forms.ChoiceField(choices=settings.STORAGE_FORMAT, required=True)
    bootable = forms.BooleanField(label=u"Is Bootable?", required=True)
    
class AddNetworkForm(forms.Form):
    name = forms.CharField(label=u"NIC Name", required=True)
    interface = forms.ChoiceField(choices=settings.NETWORK_INTERFACE_TYPE, required=True)
    network_name = forms.CharField(label=u"Network Name", required=True)
