from django.db import models

class PuppetClass(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    enabled = models.BooleanField()
    icon = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name

