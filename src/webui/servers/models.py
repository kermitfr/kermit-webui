from django.db import models
from webui.puppetclasses.models import PuppetClass
from datetime import datetime
from webui.agent.models import Agent

class Server(models.Model):
    hostname = models.CharField(max_length=255)
    os = models.CharField(max_length=255)
    architecture = models.CharField(max_length=255)
    fqdn = models.CharField(max_length=10000)
    deleted = models.BooleanField(default=False)
    icon = models.CharField(max_length=255, null=True, blank=True)
    puppet_classes = models.ManyToManyField(PuppetClass)
    agents = models.ManyToManyField(Agent)
    online = models.BooleanField(default=True)
    puppet_path = models.CharField(max_length=65000, null=True, blank=True)
    created_time = models.DateTimeField(default=datetime.now())
    updated_time = models.DateTimeField(default=datetime.now())
    
    def __unicode__(self):
        return self.hostname
    
    class Meta:
        permissions = (
            ('use_server', 'Can use server'),
        )
