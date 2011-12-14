'''
Created on Nov 16, 2011

@author: mmornati
'''
from celery.decorators import task
from webui.agent.models import Agent
import logging
from webui.agent.utils import update_info

logger = logging.getLogger(__name__)

@task()
def updateagents(user):
    logger.info("Starting Task Update Agent Info")
    agents_list = Agent.objects.filter(enabled=True)
    total_agents = len(agents_list)
    logger.info("Agents Number: %s" % total_agents)
    i = 0
    for agent in agents_list:
        update_info(user, agent, False)
        i = i + 1
        updateagents.update_state(state="PROGRESS", meta={"current": i, "total": total_agents})