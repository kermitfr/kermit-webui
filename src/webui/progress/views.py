'''
Created on Nov 17, 2011

@author: mmornati
'''
from django.http import HttpResponse
from django.utils import simplejson as json
import logging
from celery.result import AsyncResult

logger = logging.getLogger(__name__)

def get_progress(request, taskname, taskid):
    result = AsyncResult(taskid, backend=None, task_name=taskname)
    
    dict = {}
    if (result.state == 'PENDING'):
        dict['state'] = 'Waiting for worker to execute task...'
    elif (result.state == 'PROGRESS'):
        dict['state'] = 'Operation in progress..'
    else:
        dict['state'] = result.state
    if result.result:
        value = float(1.0*result.result['current']/result.result['total'])*100
        dict['value'] = value
    else: 
        dict['value'] = 0
    json_data = json.dumps(dict)
    return HttpResponse(json_data, mimetype="application/json")