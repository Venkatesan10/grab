"""
Spider task queue backend powered by redis
"""
from __future__ import absolute_import

from .base import QueueInterface
from qr import PriorityQueue
import Queue
import random

class QueueBackend(QueueInterface):
    def __init__(self, spider_name, queue_name=None, **kwargs):
        super(QueueInterface, self).__init__(**kwargs)
        self.spider_name = spider_name
        if queue_name is None:
            queue_name = 'task_queue_%s' % spider_name
        self.queue_name = queue_name
        self.queue_object = PriorityQueue(queue_name)

    def put(self, task, priority):
        # Add attribute with random value
        # This is required because qr library
        # does not allow to store multiple values with same hash
        # in the PriorityQueue
        task._rnd = random.random()
        self.queue_object.push(task, priority)

    def get(self, timeout):
        task = self.queue_object.pop()
        if task is None:
            raise Queue.Empty()
        else:
            return task

    def size(self):
        return len(self.queue_object)

    def clear(self):
        try:
            while True:
                self.get(0)
        except Queue.Empty:
            pass