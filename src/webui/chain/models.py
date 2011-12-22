from django.db import models
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime
from webui.agent.models import Agent, Action

class Scheduler(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, verbose_name="User executing or saving scheduler")
    last_run = models.DateTimeField(default=datetime.now())
    
    def __unicode__(self):
        return self.name
    
class SchedulerTask(models.Model):
    scheduler = models.ForeignKey(Scheduler, verbose_name="Referred Scheduler", blank=True, null=True, related_name='tasks')    
    agent = models.ForeignKey(Agent, verbose_name="Referred Mcollective Agent")
    action = models.ForeignKey(Action, verbose_name="Referred Mcollective Agent Action")
    parameters = models.CharField(max_length=255, null=True, blank=True)
    filters = models.CharField(max_length=255, null=True, blank=True)
