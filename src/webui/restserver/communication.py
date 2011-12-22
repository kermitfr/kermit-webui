import httplib2
from django.conf import settings
import logging
from celery.execute import send_task
from webui.restserver.tasks import httpcall
from webui.restserver.models import BackendJob
import sys

logger = logging.getLogger(__name__)

def callRestServer(user, filters, agent, action, args=None, wait_response=False, use_task=True):
    logger.info("%s is calling agent %s action %s on %s" % (user, agent, action, filters))
    
    if use_task:
        result = send_task("webui.restserver.tasks.httpcall", [filters, agent, action, args])
        logger.debug("Storing task reference in database")
        try:
            BackendJob.objects.create(user=user, task_uuid=result.task_id)
        except:
            print sys.exc_info()
            #logger.error("Error storing job in database %s" % sys.exc_info())
            
        if wait_response:
            response, content, agent, action = result.get()
        else:
            logger.debug("Returning task id. Result should be checked polling task")
            return result, 'webui.restserver.tasks.httpcall'
    else:
        logger.debug("Running MCollective call without using another task")
        response, content, agent, action = httpcall(filters, agent, action, args, use_task)
    return response, content

def verifyRestServer():
    logger.debug("Testing RestServer presence")
    http = httplib2.Http(timeout=2)
    url = settings.RUBY_REST_PING_URL
    try:
        response, content = http.request(url, "GET")
        return response.status == 200
    except:
        return False
        
    