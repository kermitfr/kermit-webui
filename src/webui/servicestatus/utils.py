'''
Created on Sep 20, 2011

@author: mmornati
'''
from webui.restserver import communication
def test_services():
    services = {}
    services['restserver'] = communication.verifyRestServer()
    return services