'''
Created on Aug 12, 2011

@author: mmornati
'''
from webui.widgets.base import Widget
import logging
from webui.restserver.models import BackendJob
import djcelery
import ast

logger = logging.getLogger(__name__)

class BackendJobHistory(Widget):
    template = "widgets/restserver/backendjob.html"
    
    def get_context(self):
        super_context = super(self.__class__,self).get_context()
        if not self.user.is_superuser:
            logger.debug("Loading just user %s information" % self.user)
            jobs = BackendJob.objects.filter(user=self.user).order_by('run_at')
        else:
            logger.debug("Admin user: loading all user history")
            jobs = BackendJob.objects.all().order_by('run_at')
            
        logger.info("Composing job information")
        jobs_list = []
        for job in jobs:
            try:
                celery_task = djcelery.models.TaskState.objects.get(task_id=job.task_uuid)
                status = celery_task.state
                arguments_list = ast.literal_eval(celery_task.args)
                arguments = {"filter":arguments_list[0],
                             "agent": arguments_list[1],
                             "action": arguments_list[2],
                             "arguments": arguments_list[3]}
            except:
                logger.error("Cannot find celery task in database. Not filled yet by celeryev")
                status = "Waiting"
                arguments = None
            job_obj = {"user": job.user,
                       "task_uuid": str(job.task_uuid),
                       "run_at": job.run_at,
                       "status": status,
                       "arguments": arguments
                       }
            jobs_list.append(job_obj)
        widget_context = {"jobs":jobs_list}
        return dict(super_context.items() + widget_context.items())
    
    
    
