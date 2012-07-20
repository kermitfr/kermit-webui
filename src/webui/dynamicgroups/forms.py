'''
Created on Jul 20, 2012

@author: mmornati
'''
from django import forms

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
    
    name = forms.CharField(label=u"DynaGroup Name", required=True)
    engine = forms.ChoiceField(label=u"Engine", required=True, choices=ENGINES)
    objname = forms.CharField(label=u"Object Name", required=True)
    rule = forms.ChoiceField(label=u"Rule", required=True, choices=RULES)
    value = forms.CharField(label=u"Value", required=False)
    force_update = forms.BooleanField(required=False,initial=False,label='Force immediately group update')
    
    

