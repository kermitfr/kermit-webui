'''
Created on Sep 9, 2011

@author: mmornati
'''
from django import forms

class SqlExecuteForm(forms.Form):
    sqllist = forms.ChoiceField(label=u"Available sqls")
    dbname = forms.CharField(label=u"Database Name")
    
class CloneDatabaseForm(forms.Form):
    instance = forms.ChoiceField(label=u"Instance Name")
    schema = forms.ChoiceField(label=u"Schema Name")
    targetserver = forms.ChoiceField(label=u"Target Server")
    targetinstance = forms.ChoiceField(label=u"Target Instance")

