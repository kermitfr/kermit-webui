from django import template
from automatix.django_widgets.loading import registry
from automatix.defaultop.widgets import DashBoardDefaultOps
from automatix.django_widgets.base import Widget, WidgetBase
register = template.Library()

@register.simple_tag
def widget(name):
    widget = registry.get_widget(name)
    return widget.render(DashBoardDefaultOps(widget))