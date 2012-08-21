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
            return convert_to_number(value) > convert_to_number(dyna_group_value)
        elif dyna_group_rule == 'lt':
            return convert_to_number(value) < dyna_group_value
        elif dyna_group_rule == 'ge':
            return convert_to_number(value) >= convert_to_number(dyna_group_value)
        elif dyna_group_rule == 'le':
            return convert_to_number(value) <= convert_to_number(dyna_group_value)
        elif dyna_group_rule == 'contains':
            return dyna_group_value in value
    
    return False
    
    
def convert_to_number(value):
    if "GB" in value or "MB" in value:
        return convert_memory(value)
    else:
        try:
            ret = int(value)
        except ValueError:
            try:
                ret = float(value)
            except ValueError:
                logger.info("Cannot convert %s to number" % value)
                ret = value
        return ret

def convert_memory(value):
    convert = False
    if "GB" in value:
        memory = value[0:value.find("GB")]
        convert = True
    elif "MB" in value:
        memory = value[0:value.find("MB")]
    else:
        memory = value
        
    logger.debug("Memory String: %s" % memory)
    try:
        ret = float(memory)
        if convert:
            ret = ret * 1024
    except ValueError:
        logger.info("Cannot convert %s to number" % value)
        ret = memory
        
    logger.debug("Memory converted: %s" % ret)
    return ret