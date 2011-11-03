'''
Created on Nov 3, 2011

@author: mmornati
'''
import logging
from django.contrib.auth.models import Group, User
from guardian.models import GroupObjectPermission, UserObjectPermission
import sys
from webui.puppetclasses.models import PuppetClass
from webui.serverstatus.models import Server
from webui.agent.models import Agent, Action

logger = logging.getLogger(__name__)

def update_acls(json_acls):
    logger.info("Updating User/Group ACLs using JSON file")
    for acl in json_acls:
        if 'group_name' in acl:
            logger.debug('ACL for group %s' % acl["group_name"])
            try: 
                current_group = Group.objects.get(name=acl['group_name'])
            except:
                logger.debug("Group %s does not exist. Creating it!" % acl['group_name'])
                current_group = Group.objects.create(name=acl['group_name'])    
            for current_class in acl["classes"]:
                try:
                    db_class = PuppetClass.objects.get(name=current_class)
                except:
                    logger.warn("Cannot find class %s in database. Need to create it first!" % current_class)
                    continue
                try:
                    GroupObjectPermission.objects.assign('access_puppet_class', current_group, db_class)
                except:
                    logger.error("Cannot assign permission: %s" % sys.exc_info())
            for current_server in acl["servers"]:
                try:
                    db_server = Server.objects.get(hostname=current_server)
                except:
                    logger.warn("Cannot find server %s in database. Need to create it first!" % current_server)
                    continue
                try:
                    GroupObjectPermission.objects.assign('use_server', current_group, db_server)
                except:
                    logger.error("Cannot assign permission: %s" % sys.exc_info())
            for current_agent in acl["agents"]:
                try:
                    db_agent = Agent.objects.get(name=current_agent)
                except:
                    logger.warn("Cannot find agent %s in database. Need to create it first!" % current_agent)
                    continue
                try:
                    GroupObjectPermission.objects.assign('use_agent', current_group, db_agent)
                except:
                    logger.error("Cannot assign permission: %s" % sys.exc_info())
            for current_action in acl["actions"]:
                try:
                    db_action = Action.objects.get(name=current_action)
                except:
                    logger.warn("Cannot find action %s in database. Need to create it first!" % current_action)
                    continue
                try:
                    GroupObjectPermission.objects.assign('use_action', current_group, db_action)
                except:
                    logger.error("Cannot assign permission: %s" % sys.exc_info())
        elif 'username' in acl:
            logger.debug('ACL for single user')
            try:
                current_user = User.objects.get(name=acl['username'])
            except:
                logger.error("User %s does not exist. Cannot assign acls!" % acl['username'])
                continue
            
            for current_class in acl["classes"]:
                try:
                    db_class = PuppetClass.objects.get(name=current_class)
                except:
                    logger.warn("Cannot find class %s in database. Need to create it first!" % current_class)
                    continue
                try:
                    UserObjectPermission.objects.assign('access_puppet_class', current_user, db_class)
                except:
                    logger.error("Cannot assign permission: %s" % sys.exc_info())
            for current_server in acl["servers"]:
                try:
                    db_server = Server.objects.get(hostname=current_server)
                except:
                    logger.warn("Cannot find server %s in database. Need to create it first!" % current_server)
                    continue
                try:
                    UserObjectPermission.objects.assign('use_server', current_user, db_server)
                except:
                    logger.error("Cannot assign permission: %s" % sys.exc_info())
            for current_agent in acl["agents"]:
                try:
                    db_agent = Agent.objects.get(name=current_agent)
                except:
                    logger.warn("Cannot find agent %s in database. Need to create it first!" % current_agent)
                    continue
                try:
                    UserObjectPermission.objects.assign('use_agent', current_user, db_agent)
                except:
                    logger.error("Cannot assign permission: %s" % sys.exc_info())
            for current_action in acl["actions"]:
                try:
                    db_action = Action.objects.get(name=current_action)
                except:
                    logger.warn("Cannot find action %s in database. Need to create it first!" % current_action)
                    continue
                try:
                    UserObjectPermission.objects.assign('use_action', current_user, db_action)
                except:
                    logger.error("Cannot assign permission: %s" % sys.exc_info())
        
    
    
