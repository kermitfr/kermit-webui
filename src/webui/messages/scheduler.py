'''
Created on Nov 12, 2012

@author: mmornati
''' 

KERMIT_SCHEDULER = {
    "check-messages": {
        "task": "webui.messages.tasks.check_kermit_base_agents",
        "period": "days",
        "every": 1,
        "args": ['CronJob']
    }
}