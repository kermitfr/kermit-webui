import httplib2
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

#TODO: Refactor using httplib address parser
def callRestServer(user, filters, agent, action, args=None):
    logger.info("%s is calling agent %s action %s on %s" % (user, agent, action, filters))
    http = httplib2.Http(timeout=20)
    url = settings.RUBY_REST_BASE_URL
    url += filters + "/"
    url += agent + "/"
    url += action + "/"
    if args:
        url += args
        logger.debug('Calling RestServer on: ' + url)
    response, content = http.request(url, "GET")
    logger.debug('Response: ' + str(response))
    logger.debug('Content: ' + str(content))
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
        
    