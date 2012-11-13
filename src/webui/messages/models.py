from django.db import models
from datetime import datetime
from webui.servers.models import Server


class MessageManager(models.Manager):
    
    def create_message(self, level, server, message):
        try:
            return Message.objects.get(server=server, level=level, message=message)
        except:
            try:
                IgnoredMessage.objects.get(server=server, message=message)
                return None
            except:
                return Message.objects.create(server=server, level=level, message=message)


#levels: 1=INFO, 2=WARNING, 3=ERROR
class Message(models.Model):
    level = models.IntegerField(default=1, null=False)
    server = models.ForeignKey(Server, verbose_name="Referred Server Node")
    time = models.DateTimeField(default=datetime.now())
    message = models.CharField(max_length=255)
    
    def __unicode__(self):
        return "%s - %s: %s" % (self.time, self.server, self.message)
    
    class Meta:
        permissions = (
            ('modify_messages', 'Can modify KermIT messages'),
        )
       
    objects = models.Manager()
    custom_objects = MessageManager() 

    
class IgnoredMessage(models.Model):
    server = models.ForeignKey(Server, verbose_name="Referred Server Node")
    message = models.CharField(max_length=255)
    
    def __unicode__(self):
        return "%s: %s" % (self.server, self.message)