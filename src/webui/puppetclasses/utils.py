import logging
from webui.puppetclasses.models import PuppetClass

logger = logging.getLogger(__name__)

def update_classes(classes_levels):
    logger.info("Deleting all actual puppet classes from database")
    PuppetClass.objects.all().delete()
    
    logger.info("Recreating puppet classes table using json file")
    for level in classes_levels:
        for pClass in level["classes"]:
            logger.debug("%s - %s" % (level, pClass))    
            currentClass = PuppetClass.objects.create(name=pClass, description=pClass, level=level["level"])
    
    