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
            
        if input['type']=='list':
            combo_values = input['validation'][1:-1].split(',')
            choices=[]
            for val in combo_values:
                val = val.strip()[1:-1]
                choices.append( (val, val) )
            fields[input['name']] = forms.ChoiceField(label=input['prompt'], required=required, choices=choices)
        else:
            fields[input['name']] = forms.RegexField(label=input['prompt'], required=required, regex=validator)
    
    return type('ActionExecutionForm', (forms.BaseForm, ), {'base_fields': fields})  