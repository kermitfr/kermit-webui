from django import template
from automatix.django_widgets.loading import registry
register = template.Library()

@register.simple_tag
def widget(name):
    widget = registry.get_widget(name)
    return widget.render()