'''
Created on Nov 12, 2012

@author: mmornati
'''
from djcelery.models import PeriodicTask, IntervalSchedule
from django.db import models

class TaskScheduler(models.Model):
    
    periodic_task = models.ForeignKey(PeriodicTask)

    @staticmethod
    def schedule_every(task_name, task, period, every, args=None, kwargs=None):
        permissible_periods = ['days', 'hours', 'minutes', 'seconds']
        if period not in permissible_periods:
            raise Exception('Invalid period specified')
        # create the periodic task and the interval
        interval_schedules = IntervalSchedule.objects.filter(period=period, every=every)
        if interval_schedules: # just check if interval schedules exist like that already and reuse em
            interval_schedule = interval_schedules[0]
        else: # create a brand new interval schedule
            interval_schedule = IntervalSchedule()
            interval_schedule.every = every # should check to make sure this is a positive int
            interval_schedule.period = period 
            interval_schedule.save()
        ptask = PeriodicTask(name=task_name, task=task, interval=interval_schedule)
        if args:
            ptask.args = args
        if kwargs:
            ptask.kwargs = kwargs
        ptask.save()
        return TaskScheduler.objects.create(periodic_task=ptask)

    def stop(self):
        """ pauses the task """
        ptask = self.periodic_task
        ptask.enabled = False
        ptask.save()

    def start(self):
        ptask = self.periodic_task
        ptask.enabled = True
        ptask.save()

    def terminate(self):
        self.stop()
        ptask = self.periodic_task
        self.delete()
        ptask.delete()