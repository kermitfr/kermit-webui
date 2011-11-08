'''
Created on Nov 7, 2011

@author: mmornati
'''
from webui.alerting.abstracts import AlertJob
from webui.alerting.models import Alert
from django.contrib.auth.models import User
import sys
class AlertScheduler(object):
    
    def register(self, alert_class):
        """
        Register the given Alert
        """
        alert_instance = alert_class()
        
        if not isinstance(alert_instance, AlertJob):
            raise TypeError("You can only register an AlertJob not a %r" % alert_class)
        complete_class_name = str(alert_instance.__class__.__name__)
        module_name = alert_instance.__module__
        alert, created = Alert.objects.get_or_create(name=complete_class_name, module=module_name)
        if created:
            admin_user = User.objects.get(username='admin')
            alert.users = [admin_user]   
            alert.run_frequency = alert_instance.run_frequency
            alert.template='server_mail.html'
        
        alert.save()


alertScheduler = AlertScheduler()

