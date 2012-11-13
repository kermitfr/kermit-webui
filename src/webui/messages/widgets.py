'''
Created on Aug 22, 2011

@author: mmornati
'''
from webui.widgets.base import Widget
import logging
from django.template.loader import get_template
from django.template.context import Context
from webui.messages.models import Message

logger = logging.getLogger(__name__)

class MessagesWidget(Widget):
    template = "widgets/messages/status.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        return dict(super_context.items())
    
    def render(self, args):
        logger.debug('Calling override render for ' + __name__)
        template_instance = get_template(self.template)
        data = self.get_context()
        data.update(widget=self, user=self.user, hostname=args)
        
        messages = Message.objects.all().order_by("-time")
        data.update(messages=messages)
        return template_instance.render(Context(data))