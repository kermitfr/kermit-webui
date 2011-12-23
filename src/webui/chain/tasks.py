'''
Created on Dec 20, 2011

@author: mmornati
'''

from celery.decorators import task
import logging
from webui.restserver.communication import callRestServer
from django.utils import simplejson as json
from datetime import datetime

logger = logging.getLogger(__name__)

@task()
def execute_chain_ops(scheduler):
    total_operations = len(scheduler.tasks.values())
    i = 0
    response_list = []
    execute_chain_ops.update_state(state="PROGRESS", meta={"current": i, "total": total_operations})
    scheduler.last_run = datetime.now() 
    scheduler.status = "RUNNING"
    scheduler.save()
    errors = False
    for op in scheduler.tasks.iterator():
        op.run_at = datetime.now()
        op.save()
        scheduler.task_running = op.order
        response, content = callRestServer(scheduler.user, op.filters, op.agent, op.action, op.parameters, True)
        if response.status == 200:
            json_content = json.loads(content)
            if json_content[0]["statuscode"] == 0:
                op.status = "SUCCESS"
                response_list.append({"name": op.name, "message": json_content[0]["statusmsg"]})
            else:
                scheduler.status = "FAILURE"
                scheduler.save()
                op.status = "FAILURE"
                op.save()
                response_list.append({"name": op.name, "message": json_content[0]["statusmsg"]})
                execute_chain_ops.update_state(state="FAILURE", meta={"current": i, "total": total_operations})
                errors = True
                break
        else:
            scheduler.status = "FAILURE"
            scheduler.save()
            response_list.append({"name": op.name, "message": "Error executing operation"})
            execute_chain_ops.update_state(state="FAILURE", meta={"current": i, "total": total_operations})
            errors = True
            break
        i = i + 1
        execute_chain_ops.update_state(state="PROGRESS", meta={"current": i, "total": total_operations})
    
    if not errors:
        scheduler.status = "COMPLETED"
        scheduler.save()
    return response_list
        