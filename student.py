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


'''
StudentLFA
'''


class StudentLFA:

    def __init__(self, id, nA):
        self.id = id
        self.nA = nA
        self.counts = np.array([0. for _ in range(self.nA + 1)])
        self.counts[self.nA] += 1

    def runActivity(self, activity):
        success = random.random() < utils.proba(activity, self.counts)
        self.counts[activity.id] += 1.
        return (1. if success else 0.)

    def getState(self):
        return np.copy(self.counts)
