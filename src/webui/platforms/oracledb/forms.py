'''
Created on Sep 9, 2011

@author: mmornati
'''
from django import forms

class SqlExecuteForm(forms.Form):
    sqllist = forms.ChoiceField(label=u"Available sqls", required=True)
    dbname = forms.CharField(label=u"Database Name", required=True)
    
class CloneDatabaseForm(forms.Form):
    instance = forms.ChoiceField(label=u"Instance Name", required=True)
    schema = forms.ChoiceField(label=u"Schema Name", required=True)
    targetserver = forms.ChoiceField(label=u"Target Server", required=True)
    targetinstance = forms.ChoiceField(label=u"Target Instance", required=True)

