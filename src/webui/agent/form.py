from django import forms

def create_action_form(inputs):
    fields = {}
    for input in inputs:
        required = not input['optional']
        max_length = int(input['max_length'])
        validator = input['validation']
        fields[input['name']] = forms.RegexField(label=input['prompt'], required=required, regex=validator)
    
    return type('ActionExecutionForm', (forms.BaseForm, ), {'base_fields': fields})  