from django.db import models
from django.contrib.auth.models import User

class Scheduler(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, verbose_name="User executing or saving scheduler")
    last_run = models.DateTimeField(null=True, blank=True)
    task_running = models.IntegerField(default=0)
    status = models.CharField(max_length=255, null=True, blank=True)
    #TaskUUID linked with djcelery.models.TaskState
    #We don't create a foreign key because the djcelery table is filled up by 
    #an external job (so it's not directly present) 
    task_uuid = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name
    
class SchedulerTask(models.Model):
    order = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    scheduler = models.ForeignKey(Scheduler, verbose_name="Referred Scheduler", blank=True, null=True, related_name='tasks')    
    agent = models.CharField(max_length=255, verbose_name="Referred Mcollective Agent")
    action = models.CharField(max_length=255, verbose_name="Referred Mcollective Agent Action")
    parameters = models.CharField(max_length=255, null=True, blank=True)
    filters = models.CharField(max_length=255, null=True, blank=True)
    run_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    result = models.CharField(max_length=255, null=True, blank=True)
