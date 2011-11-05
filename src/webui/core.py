'''
Created on Nov 3, 2011

@author: mmornati
'''
import logging

logger = logging.getLogger(__name__)

class KermitModule(object):

    def __init__(self, name=None, platform_name=None):
        self._registry = {} 
        self.root_path = None
        self.name = name

    def register(self, core_class):
        group_class = core_class.__base__
        if group_class in self._registry: 
            self._registry[group_class].append(core_class())
        else:
            self._registry[group_class] = [core_class()]

    
    def extract(self, base_class):
        if base_class in self._registry:
            return self._registry[base_class]
        else:
            logger.warn("No class registered with %s BaseClass" % base_class)
        
        return None
                
        

kermit_modules = KermitModule()