from django.db import models
from datetime import datetime

class Agent(models.Model):
    name = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    icon = models.CharField(max_length=255, null=True, blank=True)
    created_time = models.DateTimeField(default=datetime.now())
    updated_time = models.DateTimeField(default=datetime.now())
    
    def __unicode__(self):
        return self.name
    
class Action(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, null=True, blank=True)
    agent = models.ForeignKey(Agent, verbose_name="Referred Mcollective Agent", blank=True, null=True, related_name='actions')
    
    def __unicode__(self):
        return self.name
    
class ActionOutput(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, null=True, blank=True)
    display_as = models.CharField(max_length=1000)
    action = models.ForeignKey(Action, verbose_name="Referred Mcollective Agent Action", blank=True, null=True, related_name='outputs')
    
    def __unicode__(self):
        return self.name
    
class ActionInput(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, null=True, blank=True)
    type = models.CharField(max_length=255)
    prompt = models.CharField(max_length=1000)
    optional = models.BooleanField(default=False)
    validation = models.CharField(max_length=255, null=True, blank=True)
    max_length = models.IntegerField(null=True, blank=True)
    action = models.ForeignKey(Action, verbose_name="Referred Mcollective Agent Action", blank=True, null=True, related_name='inputs')
    
    def __unicode__(self):
        return self.name
    