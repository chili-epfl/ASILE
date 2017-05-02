import random
import math

class Event:

    def __init__(self, activity, student, result):
        self.activity = activity
        self.student = student
        self.result = result

    def __str__(self):
        return str({
            'a': self.activity.id,
            's': self.student,
            'r': self.result
        })
