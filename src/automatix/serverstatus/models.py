from django.db import models
from automatix.puppetclasses.models import PuppetClass

class Agent(models.Model):
    name = models.CharField(max_length=255)

class Server(models.Model):
    hostname = models.CharField(max_length=255)
    os = models.CharField(max_length=255)
    architecture = models.CharField(max_length=255)
    deleted = models.BooleanField()
    icon = models.CharField(max_length=255)
    classes = models.ManyToManyField(PuppetClass)
    agents = models.ManyToManyField(Agent)
    
    def __unicode__(self):
        return self.name