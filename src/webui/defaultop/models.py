from django.db import models
from datetime import datetime
from webui.agent.models import Agent, Action

class Operation(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    enabled = models.BooleanField(default=True)
    icon = models.CharField(max_length=255, null=True, blank=True, default="Platform_up_16.png")
    agent = models.ForeignKey(Agent, verbose_name="Referred Mcollective Agent")
    action = models.ForeignKey(Action, verbose_name="Referred Mcollective Agent Action")
    parameters = models.CharField(max_length=255, null=True, blank=True)
    filters = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=datetime.now())
    updated_time = models.DateTimeField(default=datetime.now())
    
    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ('execute_operation', 'Can execute operation'),
        )