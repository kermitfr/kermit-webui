'''
Created on Jul 20, 2012

@author: mmornati
'''
import logging

logger = logging.getLogger(__name__)

def evaluate_response(value, dyna_group_rule, dyna_group_value):
    logger.debug("Evaluating rule using %s" % value)
    if value:
        if dyna_group_rule == 'eq':
            return value == dyna_group_value
        elif dyna_group_rule == 'gt':
            return value > dyna_group_value
        elif dyna_group_rule == 'lt':
            return value < dyna_group_value
        elif dyna_group_rule == 'ge':
            return value >= dyna_group_value
        elif dyna_group_rule == 'le':
            return value <= dyna_group_value
        elif dyna_group_rule == 'contains':
            return dyna_group_value in value
    
    return False
    