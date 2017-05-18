import random
import math


class Event:

    def __init__(self, activity=None, student=None, result=True, state=None, date=None):
        self.activity = activity
        self.student = student
        self.result = result
        self.state = state
        self.date = date

    def __str__(self):
        return str({
            'a': self.activity.id,
            's': self.student.id,
            'r': self.result,
            'st': self.state
        })
