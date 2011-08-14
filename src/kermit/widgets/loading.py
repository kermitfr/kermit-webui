import copy

from django.conf import settings

class WidgetCache(object):
    def __init__(self):
        self.discovered = False
        self.widgets = {}

    def register(self, name, widget):
        """
        Register the widget in cache for later use.
        """
        if name in self.widgets:
            raise KeyError, "Only one widget named %s can be registered." % name
        self.widgets[name] = widget

    def discover_widgets(self):
        if self.discovered:
            return
        for app in settings.INSTALLED_APPS:
            # Just loading the module will do the trick
            __import__(app, {}, {}, ['widgets'])
        self.discovered = True

    def get_all_widgets(self):
        self.discover_widgets()
        return self.widgets.values()

    def get_widget(self, name):
        """
        Retrieve a widget from the cache.
        """
        self.get_all_widgets()
        return self.widgets[name]

registry = WidgetCache()
