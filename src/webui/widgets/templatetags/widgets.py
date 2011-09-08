from django import template
from webui.widgets.loading import registry
register = template.Library()

@register.simple_tag
def widget(name, user, args = None):
    widget = registry.get_widget(name)
    #TODO: Verify if multiusers cause problems
    widget.user=user
    return widget.render(args)
