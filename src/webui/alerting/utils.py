'''
Created on Nov 17, 2011

@author: mmornati
'''
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import get_template
from django.template.context import Context
from webui.alerting.models import Alert
from guardian.shortcuts import get_objects_for_user
from webui.puppetclasses.models import PuppetClass
from webui.platforms.platforms import platforms
from webui.platforms.abstracts import Application
from webui.utils import CONF
import logging

logger = logging.getLogger(__name__)

def send_server_inventory_email():
    alert_db = Alert.objects.get(name='ServerListMailAlert')
    if alert_db.enabled:
        htmly = get_template('alerting/serveremail.html')
        #Extract first level puppet class for user.
        for user in alert_db.users.all():
            servers_for_mail = []
            first_level_classes = get_objects_for_user(user, 'access_puppet_class', PuppetClass).filter(enabled=True, level=0)
            second_level_classes = get_objects_for_user(user, 'access_puppet_class', PuppetClass).filter(enabled=True, level=1)
            for first_level_class in first_level_classes:
                for second_level_class in second_level_classes:
                    server_path='/'+first_level_class.name+'/'+second_level_class.name
                    app_modules = platforms.extract(Application)
                    applications = []
                    if app_modules:
                        for current_module in app_modules:
                            applications_list = current_module.getApplicationsPath(user, server_path)
                            if applications_list:
                                applications.extend(applications_list)
                    if len(applications)>0:
                        servers_for_mail.append({'first_level_class': first_level_class.name,
                                            'second_level_class': second_level_class.name,
                                            "applications":applications})
            if len(servers_for_mail)>0:
                d = Context({ 'classed_servers': servers_for_mail })
            
                try:
                    from_email = CONF.get('webui', 'alerting.from_mail')
                except:
                    logger.warn("No from_mail configured in your webui config file. Using default")
                    from_email='no-reply@kermit.fr'
                subject = alert_db.mail_subjet
                html_content = htmly.render(d)
                msg = EmailMultiAlternatives(subject, "Need HTML", from_email, [user.email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            else:
                logger.info("Mail for user %s won't be send. No applications found!" % user.username)