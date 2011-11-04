'''
Created on Nov 3, 2011

@author: mmornati
'''
import logging

logger = logging.getLogger(__name__)

class Platform(object):

    def __init__(self, name=None, platform_name=None):
        self._registry = {} 
        self.root_path = None
        self.name = name

    def register(self, platform_class, platform):
        group_class = platform_class.__base__
        if group_class in self._registry: 
            self._registry[group_class][platform] = platform_class()
        else:
            self._registry[group_class] = {platform:platform_class()}

    
    def extract(self, base_class, platform=None):
        if platform:
            if base_class in self._registry and platform in self._registry[base_class]:
                return self._registry[base_class][platform]
            else:
                logger.warn("No class registered with %s BaseClass and %s platform" % (base_class, platform))
                return None
        else:
            platforms_classes = []
            if base_class in self._registry:
                for plat, model_class in self._registry[base_class].items():
                    platforms_classes.append(model_class)
            else:
                logger.warn("No class registered with %s BaseClass" % base_class)
            
            return platforms_classes
                
        

platforms = Platform()