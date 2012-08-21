from celery.decorators import task
from webui.restserver.communication import callRestServer
import logging
from webui.dynamicgroups.models import DynaGroup
from webui.dynamicgroups import utils
from webui.serverstatus.models import Server

logger = logging.getLogger(__name__)


@task
def update_dyna_group(user):
    try:
        i = 0
        dynagroups = DynaGroup.objects.all()
        total_groups = len(dynagroups)
        for dynag in dynagroups:
            update_single_dyna(user, dynag)
            i = i + 1
            update_dyna_group.update_state(state="PROGRESS", meta={"current": i, "total": total_groups})
      
    except Exception, err:
        logger.error('ERROR: ' + str(err))
        
def update_single_dyna(user, dynag):
    dynag.servers.clear()
    if dynag.engine == 'Facter':
        response, content = callRestServer(user, "no-filter", 'rpcutil', 'get_fact', "fact=%s" % dynag.obj_name, True, False)
        if response.getStatus() == 200:
            for sresp in content:
                if sresp.getData()["value"] and utils.evaluate_response(sresp.getData()["value"], dynag.rule, dynag.value):
                    logger.info("Rule match for %s" % sresp.getSender())
                    try:
                        server = Server.objects.get(hostname=sresp.getSender())
                    except:
                        try:
                            server = Server.objects.get(fqdn=sresp.getSender())
                        except:
                            logger.warn("Cannot find server %s in database" % sresp.getSender())
                            continue
                    
                    dynag.servers.add(server)