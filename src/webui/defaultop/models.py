from django.db import models

class Operation(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    enabled = models.BooleanField()
    icon = models.CharField(max_length=255)
    url = models.CharField(max_length=65000)
    with_template = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name
