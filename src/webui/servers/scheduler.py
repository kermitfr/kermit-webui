'''
Created on Nov 12, 2012

@author: mmornati
''' 

KERMIT_SCHEDULER = {
    "check-servers-online": {
        "task": "webui.servers.tasks.check_online",
        "period": "hours",
        "every": 1,
        "args": ['CronJob']
    }
}