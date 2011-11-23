import httplib2
from django.conf import settings
import logging
from celery.execute import send_task

logger = logging.getLogger(__name__)

#TODO: Refactor using httplib address parser
def callRestServer(user, filters, agent, action, args=None, wait_response=True):
    logger.info("%s is calling agent %s action %s on %s" % (user, agent, action, filters))
    result = send_task("webui.restserver.tasks.httpcall", [filters, agent, action, args])
    if wait_response:
        response, content = result.get()
    else:
        logger.debug("Returning task id. Result should be checked polling task")
        return result, ''
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
        
    