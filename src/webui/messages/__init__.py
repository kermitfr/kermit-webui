import logging
from webui import settings
import sys
from webui.scheduler.models import TaskScheduler

logger = logging.getLogger(__name__)

BASE_PLATFORM_PATH = "webui.platforms"
MODULES_TO_IMPORT = ["tree", "updates", "applications", "operations"]

def initialize():
    logger.info("Initializing Messages environment")
    """
    Auto-discover messages Tasks.
    """

    for app in settings.INSTALLED_APPS:
        try:
            __import__("%s.scheduler" % app)
            sched = sys.modules["%s.scheduler" % app]
            sched_var = getattr(sched, "KERMIT_SCHEDULER")
            for key, value in sched_var.items():
                try:
                    TaskScheduler.objects.get(periodic_task__name__exact=key)
                    logger.debug("Periodic task with name %s already added to database" % key)
                except:
                    logger.info("Adding task '%s' for module %s" % (key, app))
                    str_args = "[]"
                    if "args" in value and value["args"]:
                        str_args = str(value["args"]).replace('(','[').replace(')',']').replace('\'','"')
                    ts = TaskScheduler.schedule_every(task_name=key, task=value["task"], period=value["period"], every=value["every"], args=str_args)
                    logger.debug("Starting scheduler")
                    ts.start()
                    
        except ImportError:
            continue
        except:
            logger.error("Module %s has not correctly defined the KERMIT_SCHEDULER variable!" % app)
            logger.error(sys.exc_info())

