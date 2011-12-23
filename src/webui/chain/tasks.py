'''
Created on Dec 20, 2011

@author: mmornati
'''

from celery.decorators import task
import logging
from webui.restserver.communication import callRestServer
from django.utils import simplejson as json
from datetime import datetime
import time

logger = logging.getLogger(__name__)

@task()
def execute_chain_ops(scheduler, task_id=None):
    total_operations = len(scheduler.tasks.values())
    i = 0
    response_list = []
    execute_chain_ops.update_state(state="PROGRESS", meta={"current": i, "total": total_operations})
    scheduler.last_run = datetime.now() 
    scheduler.status = "RUNNING"
    scheduler.task_uuid = task_id
    scheduler.save()
    errors = False
    for op in scheduler.tasks.iterator():
        if errors:
            execute_chain_ops.update_state(state="FAILURE", meta={"current": i, "total": total_operations})
            break
        
        if op.status and op.status=='SUCCESS':
            logger.debug("Operation already completed. Skipping")
            continue
        op.run_at = datetime.now()
        op.status = "RUNNING"
        op.save()
        scheduler.task_running = i + 1
        scheduler.save()
        response, content = callRestServer(scheduler.user, op.filters, op.agent, op.action, op.parameters, True, False)
        if response.status == 200:
            json_content = json.loads(content)
            if json_content:
                operation_success = True
                servers_data = []
                for server_data in json_content:
                    if server_data["statuscode"] == 0:
                        servers_data.append(server_data)
                    else:
                        operation_success = False
                        servers_data.append(server_data)
                        errors = True
                
                response_list.append({"name": op.name, "messages": servers_data})
                if operation_success:
                    op.status = "SUCCESS"
                    op.result = servers_data
                    op.save()
                else:
                    scheduler.status = "FAILURE"
                    scheduler.save()
                    op.status = "FAILURE"
                    op.result = servers_data
                    op.save()
            #Fix for restart operation
            if op.action == 'stopinstance':
                time.sleep(10)
                    
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
        