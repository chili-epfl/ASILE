import random
import math


class Event:

    def __init__(self, activity=None, student=None, result=True, counts=None):
        self.activity = activity
        self.student = student
        self.result = result
        self.counts = counts

    def __str__(self):
        return str({
            'a': self.activity.id,
            's': self.student.id,
            'r': self.result,
            'c': self.counts
        })
