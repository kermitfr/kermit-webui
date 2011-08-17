from django.template.loader import get_template
from django.template.context import Context
from django.core.exceptions import ImproperlyConfigured
from webui.widgets import loading
from django.conf import settings

class WidgetBase(type):
    def __new__(cls, name, bases, attrs):        
        # Make sure the Widget was specified properly
        if 'template' not in attrs:
            raise ImproperlyConfigured, "%s must specify a template." % name
        # Create the class.
        widget = type.__new__(cls, name, bases, attrs)
        # Register the class for future reference
        loading.registry.register(name, widget('fooUser'))
        return widget

class Widget(object):
    __metaclass__ = WidgetBase
    template = ""
    login_required = False
    db_reference = None
    
    def __init__(self, user):
        self.user = user
        
    def get_context(self):
        """
        Provide any additional context required by the widget.
        This would be overridden when necessary.
        """
        return {"settings": settings}

    def render(self):
        """
        Render the widget's template and return the rendered contents.
        """
        template = get_template(self.template)
        data = self.get_context()
        data.update(widget=self, user=self.user)
        return template.render(Context(data))
