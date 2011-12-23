from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class BackendJob(models.Model):
    user = models.ForeignKey(User, verbose_name="User executing job")
    run_at = models.DateTimeField(default=datetime.now())
    #TaskUUID linked with djcelery.models.TaskState
    #We don't create a foreign key because the djcelery table is filled up by 
    #an external job (so it's not directly present) 
    task_uuid = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.task_uuid
