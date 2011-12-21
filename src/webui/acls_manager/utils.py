'''
Created on Nov 3, 2011

@author: mmornati
'''
import logging
from django.contrib.auth.models import Group, User, Permission
from guardian.models import GroupObjectPermission, UserObjectPermission
import sys
from webui.puppetclasses.models import PuppetClass
from webui.serverstatus.models import Server
from webui.agent.models import Agent, Action
from django.contrib.contenttypes.models import ContentType

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
                current_user = User.objects.get(username=acl['username'])
            except:
                logger.error("User %s does not exist. Cannot assign acls!" % acl['username'])
                continue
            add_acl(acl, None, current_user)
        
            
def add_acl(acl, group=None, user=None):
    logger.debug("Verifying Class ACLs")
    for current_class in acl["classes"]:
        if current_class != HERITABLE_CHAR:
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
        else:
            logger.debug("Assign permission to all classes")
            first_level_classes = PuppetClass.objects.filter(level=0)
            for first_l_class in first_level_classes:
                try:
                    if group:
                        GroupObjectPermission.objects.assign('access_puppet_class', group, first_l_class)
                    if user:
                        UserObjectPermission.objects.assign('access_puppet_class', user, first_l_class)
                except:
                    logger.error("Cannot assign permission: %s" % sys.exc_info())
                add_sub_classes_acls(first_l_class, group, user)
                
            
            
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
    assign_mco_call = False
    for current_agent, agent_actions in acl["agents"].iteritems():
        if current_agent != HERITABLE_CHAR:
            logger.debug("Assign ACL on single agent: %s" % current_agent)
            try:
                db_agent = Agent.objects.get(name=current_agent)
            except:
                logger.warn("Cannot find agent %s in database. Need to create it first!" % current_agent)
                continue
            add_agent_acl(db_agent, group, user)
        else:
            logger.debug("Assign permission to all agents")
            all_agents = Agent.objects.filter(enabled=True)
            for agent in all_agents:
                add_agent_acl(agent, group, user)
            
        for action in agent_actions:
            if action != HERITABLE_CHAR:
                if current_agent != HERITABLE_CHAR:
                    logger.debug("Assign single action acl")
                    try:
                        db_action = Action.objects.get(name=action, agent=db_agent)
                    except:
                        logger.warn("Cannot find action %s in database. Need to create it first!" % action)
                        continue
                    add_action_acl(db_action, group, user)
                    assign_mco_call = True
                else:
                    logger.warn("Cannot assign single action acl with all agents specified")
            else:
                if current_agent != HERITABLE_CHAR: 
                    logger.debug("Assign permission to all agent actions (agent: %s)" % current_agent)
                    all_agent_actions = Action.objects.filter(agent=db_agent)
                else:
                    logger.debug("Assign permission to all agents actions)")
                    all_agent_actions = Action.objects.all()
                    
                for current_action in all_agent_actions:
                    add_action_acl(current_action, group, user)
                    assign_mco_call = True
    if assign_mco_call:
        logger.debug("Assign at least one Mcollective action. Adding call_mcollective acl")
        try:
            agent_ct = ContentType.objects.get(model='agent')
            call_mco_perm = Permission.objects.get(codename="call_mcollective", content_type=agent_ct)
            if group:
                group.permissions.add(call_mco_perm)
            if user:
                user.user_permissions.add(call_mco_perm)
        except:
            print sys.exc_info()   
        
         
def add_agent_acl(agent, group=None, user=None):   
    try:
        if group:
            GroupObjectPermission.objects.assign('use_agent', group, agent)
        if user:
            UserObjectPermission.objects.assign('use_agent', user, agent)
    except:
        logger.error("Cannot assign permission: %s" % sys.exc_info())

def add_action_acl(action, group=None, user=None):
    try:
        if group:
            GroupObjectPermission.objects.assign('use_action', group, action)
        if user:
            UserObjectPermission.objects.assign('use_action', user, action)
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
        new_class_name = puppet_class.rstrip(HERITABLE_CHAR)
    try:
        db_class = PuppetClass.objects.get(name=new_class_name)
    except:
        logger.warn("Cannot find class %s in database. Need to create it first!" % new_class_name)
        db_class = None
    return heritable, db_class
    
