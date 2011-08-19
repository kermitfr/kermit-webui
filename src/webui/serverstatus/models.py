from django.db import models
from webui.puppetclasses.models import PuppetClass
from datetime import datetime

class Agent(models.Model):
    name = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    icon = models.CharField(max_length=255, null=True)
    created_time = models.DateTimeField(default=datetime.now())
    updated_time = models.DateTimeField(default=datetime.now())
    
    def __unicode__(self):
        return self.name

class Server(models.Model):
    hostname = models.CharField(max_length=255)
    os = models.CharField(max_length=255)
    architecture = models.CharField(max_length=255)
    fqdn = models.CharField(max_length=10000)
    deleted = models.BooleanField(default=False)
    icon = models.CharField(max_length=255, null=True)
    puppet_classes = models.ManyToManyField(PuppetClass)
    agents = models.ManyToManyField(Agent)
    online = models.BooleanField(default=True)
    puppet_path = models.CharField(max_length=65000, null=True)
    created_time = models.DateTimeField(default=datetime.now())
    updated_time = models.DateTimeField(default=datetime.now())
    
    def __unicode__(self):
        return self.hostname
