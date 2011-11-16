'''
Created on Nov 16, 2011

@author: mmornati
'''
from celery.decorators import task

@task()
def add(x, y):
    return x + y