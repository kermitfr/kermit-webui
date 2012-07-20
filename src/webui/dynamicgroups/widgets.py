'''
Created on Jul 20, 2012

@author: mmornati
'''
from webui.widgets.base import Widget

class DynaGroupTree(Widget):
    template = "widgets/dynagroups/dynagroupstree.html"
    permissions = ['agent.show_widget_dynagroup']
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        return dict(super_context.items())
    
    
    
