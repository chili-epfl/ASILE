import random
import math
import utils

from simulation import Simulation
from model import Model

from activity import *
from student import *
from event import *
from model import *

'''
Optimizer
'''


class Optimizer:

    def __init__(self, nA):
        self.nA = nA
        self.history = {}

    def nextActivity(self, studentID):
        raise Exception('Parent method not implemented')

    def submitResult(self, studentID, activityID, result):
        raise Exception('Parent method not implemented')


'''
RandomOptimizer
'''


class RandomOptimizer(Optimizer):

    def __init__(self, nA):
        self.nA = nA
        self.history = {}

    def nextActivity(self, studentID):
        if studentID not in self.history:
            self.history[studentID] = set()
        available = list(set(range(1, self.nA)) - self.history[studentID])
        nextA = random.choice(available) if len(available) > 0 else None
        return nextA

    def submitResult(self, studentID, activityID, result):
        if studentID not in self.history:
            self.history[studentID] = set()
        if(result == 1):
            self.history[studentID].add(activityID)


'''
Bandit Optimizer
'''


class BanditOptimizer(Optimizer):

    def __init__(self, nA):
        self.nA = nA
        self.model = ModelLFA(nA)
        for id in range(nA):
            self.model.activities[id] = self.model.getActivityModel(id)
        self.count = 1
        self.activityCounts = [1 for _ in range(self.nA)]
        self.fitCount = 2

    def nextActivity(self, studentID):
        optActivities = [None]
        optScore = -10.

        state = self.model.students[studentID].getState(None) if studentID in self.model.students else {}
        available = [a.id for a in self.model.activities.values() if a.id not in state and a.id != 0]

        for activityID in available:
            confidence = (2. * math.log(self.count) / self.activityCounts[activityID]) ** 0.5
            param = 1. / (1 + math.exp(- self.model.activities[0].params[activityID] - self.model.activities[0].params[-1]))
            score = param + confidence

            if score > optScore:
                optScore = score
                optActivities = [ activityID ]
            elif score > optScore - 1e-4:
                optActivities.append(activityID)

        choice = random.choice(optActivities)

        return choice

    def submitResult(self, studentID, activityID, result):
        self.count += 1
        self.activityCounts[activityID] += 1
        self.model.reportEvent(studentID, activityID, result, self.count, withState=True)

        if self.activityCounts[0] > (self.fitCount ** 2.) / 4.:
            self.fitCount += 1
            self.model.activities[0].fit()


'''
Epsilon Optimizer
'''


class EpsilonOptimizer(Optimizer):

    def __init__(self, nA, nS, eps):
        self.nA = nA
        self.nS = nS
        self.eps = eps
        self.model = ModelLFA(nA)
        for id in range(nA):
            self.model.activities[id] = self.model.getActivityModel(id)

        self.count = 1
        self.studentCount = 0
        self.fitted = False

    def nextActivity(self, studentID):
        state = self.model.students[studentID].getState(None) if studentID in self.model.students else {}
        available = [a.id for a in self.model.activities.values() if a.id not in state and a.id != 0]

        if not self.fitted:
            return random.choice(available)

        return self.model.optimalChoice(state)

    def submitResult(self, studentID, activityID, result):
        self.count += 1
        self.model.reportEvent(studentID, activityID, result, self.count, withState=True)

        if activityID == 0:
            self.studentCount += 1

        if not self.fitted and self.studentCount > self.eps:
            self.fitted = True
            self.model.activities[0].fit()
