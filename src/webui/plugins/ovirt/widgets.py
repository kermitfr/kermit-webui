'''
Created on Aug 22, 2011

@author: mmornati
'''
from webui.widgets.base import Widget
import logging
from django.template.loader import get_template
from django.template.context import Context
from webui.plugins.ovirt.forms import CreateVMForm, AddStorageForm,\
    AddNetworkForm

logger = logging.getLogger(__name__)
    
class CreateoVirtVM(Widget):
    template = "plugins/ovirt/widgets/createwizard.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        return dict(super_context.items())
    
    def render(self, args):
        logger.debug('Calling override render for ' + __name__)
        template_instance = get_template(self.template)
        data = self.get_context()
        data.update(widget=self, user=self.user, hostname=args)
        base_form = CreateVMForm(prefix="base")
        storage_form = AddStorageForm(prefix="storage")
        network_form = AddNetworkForm(prefix="network")
        data.update(base_form=base_form, storage_form=storage_form, network_form=network_form)
        return template_instance.render(Context(data))