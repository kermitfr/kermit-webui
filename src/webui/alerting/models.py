from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    object_pk = models.CharField(ugettext_lazy('object ID'), max_length=255)
    content_object = generic.GenericForeignKey(fk_field='object_pk')

class Alert(models.Model):
    name = models.CharField(max_length=255)
    module = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    enabled = models.BooleanField(default=True)
    users = models.ManyToManyField(User, verbose_name="list of destination users")
    run_frequency = models.PositiveIntegerField(default=86400)
    last_run = models.DateTimeField(default=datetime.now())
    event = models.ForeignKey(Event, blank=True, null=True, on_delete=models.SET_NULL)
    mail_subjet = models.CharField(max_length=255)
    template = models.CharField(max_length=255)
    
