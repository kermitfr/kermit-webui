'''
Created on Nov 3, 2011

@author: mmornati
'''
import logging

logger = logging.getLogger(__name__)

class Plugin(object):

    def __init__(self, name=None, platform_name=None):
        self._registry = {} 
        self.root_path = None
        self.name = name

    def register(self, plugin_class, plugin):
        group_class = plugin_class.__base__
        if group_class in self._registry: 
            self._registry[group_class][plugin] = plugin_class()
        else:
            self._registry[group_class] = {plugin:plugin_class()}

    
    def extract(self, base_class, plugin=None):
        if plugin:
            if base_class in self._registry and plugin in self._registry[base_class]:
                return self._registry[base_class][plugin]
            else:
                logger.warn("No class registered with %s BaseClass and %s plugin" % (base_class, plugin))
                return None
        else:
            plugins_classes = []
            if base_class in self._registry:
                for plat, model_class in self._registry[base_class].items():
                    plugins_classes.append(model_class)
            else:
                logger.warn("No class registered with %s BaseClass" % base_class)
            
            return plugins_classes
                
        

plugins = Plugin()