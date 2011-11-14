'''
Created on Sep 9, 2011

@author: mmornati
'''
from django import forms

class SqlExecuteForm(forms.Form):
    sqllist = forms.ChoiceField(label=u"Available sqls")
    dbname = forms.CharField(label=u"Database Name")
