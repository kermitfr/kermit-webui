from django.db import models
from datetime import datetime

COLOR_CHOICES = (
    ('white', 'White'),
    ('yellow', 'Yellow'),
    ('red', 'Red'),
    ('blue', 'Blue'),
    ('orange', 'Orange'),
    ('green', 'Green')
)

class Widget(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    enabled = models.BooleanField(default=True)
    icon = models.CharField(max_length=255, null=True)
    color = models.CharField(max_length=255, default='white', choices=COLOR_CHOICES)
    movable = models.BooleanField(default=True)
    removable = models.BooleanField(default=True)
    editable = models.BooleanField(default=False)
    refreshable = models.BooleanField(default=False)
    refreshUrl = models.CharField(max_length=255, null=True)
    column = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=datetime.now())
    updated_time = models.DateTimeField(default=datetime.now())
    
    def __unicode__(self):
        return self.name
