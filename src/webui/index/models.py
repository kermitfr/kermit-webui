from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    order = models.IntegerField(default=50)
    url = models.URLField(verify_exists=False)
    
    def __unicode__(self):
        return self.name