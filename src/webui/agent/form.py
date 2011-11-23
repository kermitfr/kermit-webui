from django import forms

def create_action_form(inputs):
    fields = {}
    for input in inputs:
        required = not input['optional']
        if 'max_length' in input and input['max_length']:
            max_length = int(input['max_length'])
        else:
            max_length = 1000
        if 'validation' in input and input['validation']:
            validator = input['validation']
        else:
            validator = ""
        fields[input['name']] = forms.RegexField(label=input['prompt'], required=required, regex=validator)
    
    return type('ActionExecutionForm', (forms.BaseForm, ), {'base_fields': fields})  