'''
Created on Jul 20, 2012

@author: mmornati
'''
from django import forms
from django.forms.widgets import HiddenInput

class DynaGroupEditForm(forms.Form):
    ENGINES = [
       ('Facter', "Facter"),
    ]
    
    RULES = [
       ('eq', "Equals"),
       ('gt', "Greater than"),
       ('ge', "Greater equals"),
       ('lt', "Less than"),
       ('le', "Less equals"),
    ]
    
    dynag_id = forms.CharField(widget=HiddenInput, required=False)
    name = forms.CharField(label=u"DynaGroup Name", required=True)
    engine = forms.ChoiceField(label=u"Engine", required=True, choices=ENGINES)
    objname = forms.CharField(label=u"Expression", required=True, widget=forms.TextInput(attrs={'size':'50'}), help_text="<br/><b>Example</b>:  <i>(kernelversion>2.3 and operatingsystem=Fedora) or operatingsystem=CentOS</i>")
    #rule = forms.ChoiceField(label=u"Rule", required=False, choices=RULES)
    #value = forms.CharField(label=u"Value", required=False)
    force_update = forms.BooleanField(required=False,initial=False,label='Force immediately group update')
    
    

