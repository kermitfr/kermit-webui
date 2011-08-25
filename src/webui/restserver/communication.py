import httplib2
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def callRestServer(filters, agent, action, args=None):
    http = httplib2.Http(timeout=20)
    url = settings.RUBY_REST_BASE_URL
    url += filters + "/"
    url += agent + "/"
    url += action + "/"
    if args:
        url += args
        logger.debug('Calling RestServer on: ' + url)
    response, content = http.request(url, "GET")
    logger.info('Response: ' + str(response))
    logger.debug('Content: ' + str(content))
    return response, content