#mco rpc puppetagent classlist --with-id=/puppet/ --verbose
from celery.decorators import task
from webui.restserver.communication import callRestServer
from webui import settings
from webui.puppetclasses.models import PuppetClass
import logging

logger = logging.getLogger(__name__)


@task
def update_all_puppet_classes(user):
    try: 
        if settings.PUPPET_MASTER_SERVER_HOSTNAME:
            filters = 'identity_filter=%s' % settings.PUPPET_MASTER_SERVER_HOSTNAME
        else:
            logger.warn("You should specify your puppet master hostname in settings file to improve KermIT performances")
            filters = "no-filter"
        resp, content = callRestServer(user, filters, 'puppetagent', 'classlist', None, True, False)
        if resp.getStatus() == 200:
            i = 0
            total_classes = 0
            for response in content:
                if not "classlist" in response.getData():
                    continue
                total_classes = total_classes + len(response.getData()["classlist"])
                
            logger.debug("Total classes found: %s" % total_classes)
                
                
            for response in content:
                if not "classlist" in response.getData():
                    continue
                for current_class in response.getData()["classlist"]:
                    try:
                        PuppetClass.objects.get(name=current_class)
                        logger.debug("Class already present in KermIT database")
                    except:     
                        logger.debug("Cannot find class with name %s" % current_class)
                        logger.info("Creating new class %s" % current_class)
                        PuppetClass.objects.create(name=current_class)
            
                    i = i + 1
                    update_all_puppet_classes.update_state(state="PROGRESS", meta={"current": i, "total": total_classes})
                            
    except Exception, err:
        logger.error('ERROR: ' + str(err))