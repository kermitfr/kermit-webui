from django.db import models
from datetime import datetime

class Operation(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    enabled = models.BooleanField()
    icon = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=65000)
    with_template = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=datetime.now())
    updated_time = models.DateTimeField(default=datetime.now())
    
    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ('executo_operation', 'Can execute operation'),
        )