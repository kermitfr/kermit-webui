'''
Created on Dec 20, 2011

@author: mmornati
'''

from celery.decorators import task
import logging
from webui.restserver.communication import callRestServer
from django.utils import simplejson as json

logger = logging.getLogger(__name__)

@task()
def execute_chain_ops(operations):
    total_operations = len(operations)
    i = 0
    response_list = []
    execute_chain_ops.update_state(state="PROGRESS", meta={"current": i, "total": total_operations})
    for op in operations:
        response, content = callRestServer(op["user"], op["filters"], op["agent"], op["action"], op["args"], True)
        if response.status == 200:
            json_content = json.loads(content)
            response_list.append({"name": op["name"], "message": json_content[0]["statusmsg"]})
        else:
            response_list.append({"name": op["name"], "message": "Error executing operation"})
        i = i + 1
        execute_chain_ops.update_state(state="PROGRESS", meta={"current": i, "total": total_operations})
    
    return response_list
        