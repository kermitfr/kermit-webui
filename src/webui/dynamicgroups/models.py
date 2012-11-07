from django.db import models
from webui.servers.models import Server

class DynaGroup(models.Model):
    name = models.CharField(max_length=255)
    engine = models.CharField(max_length=255)
    obj_name = models.CharField(max_length=255)
    rule = models.CharField(max_length=255)
    value = models.CharField(max_length=255, null=True, blank=True)
    servers = models.ManyToManyField(Server, null=True, blank=True)
    
