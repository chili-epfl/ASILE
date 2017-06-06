import random
import math
import utils

from simulation import Simulation
from model import Model

from activity import *
from student import *
from event import *

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
        available = list(set(range(self.nA)) - self.history[studentID])
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
        self.activities = [ActivityLFA(id, self.nA) for id in range(self.nA)]

        self.history = {}

        self.students = {}

        self.events = []

        self.count = 0
        self.activityCounts = [1 for _ in range(self.nA)]
        self.shouldFit = [set() for _ in range(self.nA)]

        self.target = np.array([0. for _ in range(self.nA + 1)])
        self.targetE = np.array([0. for _ in range(self.nA + 1)])

    def nextActivity(self, studentID):
        target = self.activities[0]
        if studentID not in self.students:
            self.students[studentID] = StudentLFA(studentID, self.nA)
            self.history[studentID] = set()

        student = self.students[studentID]
        available = [aid for aid in range(
            self.nA) if aid not in self.history[studentID]]
        bestA = None
        bestS = -999999.
        for aid in available:
            a = self.activities[aid]
            if student.counts[a.id] < 1:
                score = target.p[a.id]
                if score > bestS:
                    bestA = a
                    bestS = score
        return bestA.id if bestA is not None else None

    def submitResult(self, studentID, activityID, result):
        if studentID not in self.students:
            self.students[studentID] = StudentLFA(studentID, self.nA)
            self.history[studentID] = set()

        self.count += 1
        self.activityCounts[activityID] += 1

        if(result == 1):
            self.history[studentID].add(activityID)

        ev = Event(
            activity=self.activities[activityID],
            student=self.students[studentID],
            result=result,
            counts=list(self.students[studentID].counts)
        )
        self.events.append(ev)
        ev.student.runActivity(self.activities[activityID])
        self.activities[activityID].events.append(ev)

        n = int(self.activityCounts[activityID] ** 0.5)
        if(n not in self.shouldFit[activityID] and n > 100 ** 0.5):
            # print(activityID)
            # print(self.activityCounts)
            self.shouldFit[activityID].add(n)
            self.activities[activityID].fit()

    def fit(self):
        X = [e.counts for e in self.events]
        y = [e.result for e in self.events]
        if(0. in y and 1. in y):
            logit = sm.Logit(y, X)
            result = logit.fit_regularized(disp=False, method='l1', alpha=1e-2)
            self.target = np.array(result.params)
            self.targetE = np.array(result.bse)

        print(target)
        print(targetE)

        for a in self.activities:
            a.fit()


'''
Epsilon Optimizer
'''


class EpsilonOptimizer(Optimizer):

    def __init__(self, nA, nS):
        self.nA = nA
        self.nS = nS
        self.history = {}
        self.count = 0
        for id in range(self.nS):
            self.history[id] = set()

        self.activities = [ActivityLFA(id, self.nA) for id in range(self.nA)]
        self.students = {}
        self.events = []

    def nextActivity(self, studentID):

        if studentID not in self.students:
            self.students[studentID] = StudentLFA(studentID, self.nA)
            self.history[studentID] = set()

        if self.count < int(self.nS):
            available = [aid for aid in range(
                self.nA) if aid not in self.history[studentID]]
            nextA = random.choice(available) if len(available) > 0 else None
            return nextA
        target = self.activities[0]
        student = self.students[studentID]
        available = [aid for aid in range(
            self.nA) if aid not in self.history[studentID]]
        bestA = None
        bestS = -999999.
        for aid in available:
            a = self.activities[aid]
            if student.counts[a.id] < 1:
                score = target.p[a.id]
                if score > bestS:
                    bestA = a
                    bestS = score
        return bestA.id if bestA is not None else None

    def submitResult(self, studentID, activityID, result):

        if studentID not in self.students:
            self.students[studentID] = StudentLFA(studentID, self.nA)
            self.history[studentID] = set()

        self.count += 1

        if(result == 1):
            self.history[studentID].add(activityID)

        ev = Event(
            activity=self.activities[activityID],
            student=self.students[studentID],
            result=result,
            counts=list(self.students[studentID].counts)
        )
        self.events.append(ev)
        ev.student.runActivity(self.activities[activityID])
        self.activities[activityID].events.append(ev)

        if(self.count == int(self.nS)):
            self.fit()

    def fit(self):
        for a in self.activities:
            a.fit()
