'''
Created on Nov 18, 2011

@author: mmornati
'''
import os

def check_service(name):
    g = os.popen("ps -e -o pid,command")
    pid = None
    for line in g.readlines():
        if name in line:
            pid = line.strip().split(' ')[0]
            break

    return pid