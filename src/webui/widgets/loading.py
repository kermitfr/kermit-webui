import copy

from django.conf import settings
from webui.widgets.models import Widget
import logging

logger = logging.getLogger(__name__)

class WidgetCache(object):
    def __init__(self):
        self.discovered = False
        self.widgets = {}
        self.widgets_dashboard = {}

    def register(self, name, widget):
        """
        Register the widget in cache for later use.
        """
        if name in self.widgets:
            raise KeyError, "Only one widget named %s can be registered." % name
        widget.db_reference = self.check_widget_on_db(name)
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
        return self.widgets[name]
    
    def get_widgets_dashboard(self, user):
        if not self.widgets_dashboard:
            logger.info("Loading all database widgets in memory")
            #By default just two column are supported
            for i in range(1, 3):
                col_widgets = Widget.objects.filter(column=i, enabled=True).order_by('order')
                self.widgets_dashboard[str(i)] = col_widgets.values()
        #Check user_permissions and widget permissions
        user_widgets = self.check_permissions(user)
        if user_widgets:
            return user_widgets
        else:
            return self.widgets_dashboard
    
    def check_permissions(self, user):
        user_widget = {}
        for i in range(1, 3):
            user_widget[str(i)] = []
            for widget_db in self.widgets_dashboard[str(i)]:
                widget = self.widgets[widget_db['name']]
                if len(widget.permissions)>0:
                    logger.debug("Widget %s has set permissions. User must have the right permission to use it." % widget_db['name'])
                    logger.debug("Required permissions: %s" % widget.permissions)
                    if user.has_perms(widget.permissions):
                        user_widget[str(i)].append(widget_db)
                    else:
                        logger.debug('User does not have permission to see this widget_db')
                else:
                    logger.debug('Widget %s does not have permissions. Visibile to all users' % widget_db['name'])
                    user_widget[str(i)].append(widget_db)
                    
        return user_widget
                        
                    
                    
                    
    def refresh_widgets(self):
        logger.info("Refreshing all database widgets in memory")
        #By default just two column are supported
        return Widget.objects.filter().values()
                
    
    def check_widget_on_db(self, name):
        #Also the 'abstract' widgets class is discovered
        #So we exclude this class from the widgets imported into database
        if not name == 'Widget':
            widget = Widget.objects.filter(name=name)
            if widget:
                logger.info("Widget " + name + " already present in database. Loading...")
                return widget[0]
            else:
                logger.info("New widget discovered. Adding it to database.")
                widget = Widget.objects.create(name=name, title=name, enabled=False)
                return widget

    def reset_cache(self):
        logger.info("Resetting Widget Cache")
        #self.widgets = {}
        self.widgets_dashboard = {}
        
registry = WidgetCache()
