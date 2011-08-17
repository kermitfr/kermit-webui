from django.db import models
from datetime import datetime

class PuppetClass(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    enabled = models.BooleanField()
    icon = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    order = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=datetime.now())
    updated_time = models.DateTimeField(default=datetime.now())
    
    def __unicode__(self):
        return self.name

