from django import template
from kermit.widgets.loading import registry
register = template.Library()

@register.simple_tag
def widget(name):
    widget = registry.get_widget(name)
    return widget.render()