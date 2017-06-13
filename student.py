import random
import numpy as np

import utils


'''
Student
'''


class Student:

    def __init__(self, id):
        self.id = id

    def runActivity(self, activity):
        raise Exception('Parent method not implemented')

    def getState(self):
        raise Exception('Parent method not implemented')

    def __str__(self):
        return str({
            'id': self.id,
            'states': self.states
        })


'''
StudentLFA
'''


class StudentLFA(Student):

    def __init__(self, id, D):
        self.D = D
        self.id = id
        self.events = []

    def runActivity(self, activity):
        success = random.random() < utils.proba(activity, self.counts)
        self.state[activity.id] += 1.
        return (1. if success else 0.)

    def getState(self, date):
        state = {}
        for e in self.events:
            if date is None or e.date <= date:
                state[e.activity.id] = 1 + state.get(e.activity.id, 0)
        return state
