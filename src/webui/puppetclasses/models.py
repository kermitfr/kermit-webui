from django.db import models
from datetime import datetime

class PuppetClass(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    enabled = models.BooleanField(default=True)
    icon = models.CharField(max_length=255, null=True, blank=True)
    level = models.IntegerField(default=0, null=False)
    parent = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=datetime.now())
    updated_time = models.DateTimeField(default=datetime.now())
    
    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ('access_puppet_class', 'Can access PuppetClass'),
        )
