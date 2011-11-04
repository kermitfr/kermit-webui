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

HERITABLE_CHAR = "+"

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
            add_acl(acl, current_group)     
        elif 'username' in acl:
            logger.debug('ACL for single user')
            try:
                current_user = User.objects.get(name=acl['username'])
            except:
                logger.error("User %s does not exist. Cannot assign acls!" % acl['username'])
                continue
            add_acl(acl, None, current_user)
        
            
def add_acl(acl, group=None, user=None):
    logger.debug("Verifying Class ACLs")
    for current_class in acl["classes"]:
        heritable, db_class = check_heritable(current_class)
        if db_class:
            try:
                if group:
                    GroupObjectPermission.objects.assign('access_puppet_class', group, db_class)
                if user:
                    UserObjectPermission.objects.assign('access_puppet_class', user, db_class)
            except:
                logger.error("Cannot assign permission: %s" % sys.exc_info())
            if heritable:
                logger.debug("Heritable ACL found. Adding ACLs on all sub level classes")
                add_sub_classes_acls(db_class, group, user)
            
            
    logger.debug("Verifying Server ACLs")
    for current_server in acl["servers"]:
        try:
            db_server = Server.objects.get(hostname=current_server)
        except:
            logger.warn("Cannot find server %s in database. Need to create it first!" % current_server)
            continue
        try:
            if group:
                GroupObjectPermission.objects.assign('use_server', group, db_server)
            if user:
                UserObjectPermission.objects.assign('use_server', user, db_server)
        except:
            logger.error("Cannot assign permission: %s" % sys.exc_info())
            
    logger.debug("Verifying Agent ACLs")
    for current_agent in acl["agents"]:
        try:
            db_agent = Agent.objects.get(name=current_agent)
        except:
            logger.warn("Cannot find agent %s in database. Need to create it first!" % current_agent)
            continue
        try:
            if group:
                GroupObjectPermission.objects.assign('use_agent', group, db_agent)
            if user:
                UserObjectPermission.objects.assign('use_agent', user, db_agent)
        except:
            logger.error("Cannot assign permission: %s" % sys.exc_info())
            
    logger.debug("Verifying Action ACLs")     
    for current_action in acl["actions"]:
        try:
            db_action = Action.objects.get(name=current_action)
        except:
            logger.warn("Cannot find action %s in database. Need to create it first!" % current_action)
            continue
        try:
            if group:
                GroupObjectPermission.objects.assign('use_action', group, db_action)
            if user:
                UserObjectPermission.objects.assign('use_action', user, db_action)
        except:
            logger.error("Cannot assign permission: %s" % sys.exc_info())
            

def add_sub_classes_acls(current_class, group=None, user=None):
    level = current_class.level+1
    sub_classes = PuppetClass.objects.filter(level=level)
    while sub_classes:
        for sub in sub_classes:
            if group:
                GroupObjectPermission.objects.assign('access_puppet_class', group, sub)
            if user:
                UserObjectPermission.objects.assign('access_puppet_class', user, sub) 
        level = level+1
        sub_classes = PuppetClass.objects.filter(level=level)
    
        
def check_heritable(puppet_class):
    heritable = False
    new_class_name = puppet_class
    if puppet_class.endswith(HERITABLE_CHAR):
        heritable = True
        new_class_name = puppet_class.rstrip("+")
    try:
        db_class = PuppetClass.objects.get(name=new_class_name)
    except:
        logger.warn("Cannot find class %s in database. Need to create it first!" % new_class_name)
        db_class = None
    return heritable, db_class
    
