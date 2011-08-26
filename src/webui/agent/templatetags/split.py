from django import template
from django.utils.safestring import mark_safe, SafeData
from django.template.defaultfilters import stringfilter

register = template.Library()

class SplitNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def render(self, context):
        context[self.name] = self.value
        return ''

@register.simple_tag
def split_as_option(value, splitter='|', autoescape=None):
    if not isinstance(value, SafeData):
        value = mark_safe(value)
    value = value.split(splitter)
    result = ""
    for v in value:
        result += '<option value="%s">%s</option>\n' % (v, v)
    return mark_safe(result)
split_as_option.is_safe = True
split_as_option.needs_autoescape = True

@register.simple_tag
def split_as_list(value, context_name='splitted_list', splitter=',', autoescape=None):
    if not isinstance(value, SafeData):
        value = mark_safe(value)
    value = value.split(splitter)
    return SplitNode(context_name, value)
