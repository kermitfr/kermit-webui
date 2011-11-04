'''
Created on Oct 25, 2011

@author: mmornati
'''
from webui.widgets.base import Widget
import logging
from django.template.loader import get_template
from django.template.context import Context
from webui.platforms.platforms import platforms
from webui.platforms.abstracts import Application
logger = logging.getLogger(__name__)

class ApplicationsStatus(Widget):
    template = "widgets/applications/applistatus.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        applications = []
        app_modules = platforms.extract(Application)
        if app_modules:
            for current_module in app_modules:
                applications_list = current_module.getApplications(self.user)
                if applications_list:
                    applications.extend(applications_list)
        widget_context = {"applications":applications}
        return dict(super_context.items() + widget_context.items())
    
class ApplicationDetails(Widget):
    template = "widgets/applications/applidetails.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        return dict(super_context.items())
    
    def render(self, args):
        logger.debug('Calling override render for ' + __name__)
        template_instance = get_template(self.template)
        data = self.get_context()
        appname = args
        data.update(widget=self, user=self.user, appname=appname)
        
        applications = []
        app_modules = platforms.extract(Application)
        if app_modules:
            for current_module in app_modules:
                applications_list = current_module.getAppliInfo(self.user, appname)
                if applications_list:
                    applications.extend(applications_list)
                
        data.update(applications=applications)
        return template_instance.render(Context(data))
