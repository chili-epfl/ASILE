import random
import math
import utils

import Simulation
import Model

import Activity as A
import Student as S
import Event as E

################################################
################## RANDOM ######################
################################################
class RandomOptimizer:

    def __init__(self, nA=8, nS=100):
        self.nA = nA
        self.nS = nS
        self.history = {}
        for id in range(self.nS):
            self.history[id] = set()

    def nextActivity(self, studentID):
        available = [aid for aid in range(self.nA) if not aid in self.history[studentID]]
        nextA = random.choice(available) if len(available) > 0 else None
        return nextA

    def submitResult(self, studentID, activityID, result):
        if(result == 1):
            self.history[studentID].add(activityID)

################################################
################## BANDITS #####################
################################################
class BanditOptimizer:

    def __init__(self, nA=8, nS=100):
        self.nA = nA
        self.nS = nS
        self.alpha = 2.
        self.f = 0.3
        self.activities = [A.Activity(id, self.nA) for id in range(self.nA)]
        self.students = [S.Student(id, self.nA) for id in range(self.nS)]
        self.events = []
        self.history = {}
        for id in range(self.nS):
            self.history[id] = set()
        self.count = 0
        self.activityCounts = [1 for _ in range(self.nA)]
        self.shouldFit = [set() for _ in range(self.nA)]

    def nextActivity(self, studentID):
        target = self.activities[0]
        student = self.students[studentID]
        available = [aid for aid in range(self.nA) if not aid in self.history[studentID]]
        bestA = None
        bestS = -999999.
        for aid in available:
            a = self.activities[aid]
            if student.counts[a.id] < 1:
                p = utils.proba(a, student.counts)
                score = target.p[a.id] * p + target.p[self.nA + a.id] * (1 - p) + self.alpha * random.random() * math.log(1 + self.count) / self.activityCounts[a.id]
                if score > bestS:
                    bestA = a
                    bestS = score
        return bestA.id if bestA is not None else None

    def submitResult(self, studentID, activityID, result):
        self.count += 1
        self.activityCounts[activityID] += 1

        if(result == 1):
            self.history[studentID].add(activityID)
        
        ev = E.Event(
            activity=self.activities[activityID],
            student=self.students[studentID],
            result=result,
            counts=list(self.students[studentID].counts)
        )
        self.events.append(ev)
        ev.student.runActivity(ev)
        self.activities[activityID].events.append(ev)

        n = int(self.activityCounts[activityID] ** self.f)
        if(n not in self.shouldFit[activityID] and n > 100 ** self.f):
            #print(activityID)
            #print(self.activityCounts)
            self.shouldFit[activityID].add(n)
            self.activities[activityID].fit()

    def fit(self):
        print(self.count)
        print(self.activityCounts)
        for a in self.activities:
            a.fit()

################################################
################## EPSILON #####################
################################################
class EpsilonOptimizer:

    def __init__(self, nA=8, nS=100):
        self.nA = nA
        self.nS = nS
        self.history = {}
        self.count = 0
        for id in range(self.nS):
            self.history[id] = set()

        self.activities = [A.Activity(id, self.nA) for id in range(self.nA)]
        self.students = [S.Student(id, self.nA) for id in range(self.nS)]
        self.events = []

    def nextActivity(self, studentID):
        if self.count < int(self.nS):
            available = [aid for aid in range(self.nA) if not aid in self.history[studentID]]
            nextA = random.choice(available) if len(available) > 0 else None
            return nextA
        target = self.activities[0]
        student = self.students[studentID]
        available = [aid for aid in range(self.nA) if not aid in self.history[studentID]]
        bestA = None
        bestS = -999999.
        for aid in available:
            a = self.activities[aid]
            if student.counts[a.id] < 1:
                p = utils.proba(a, student.counts)
                score = target.p[a.id] * p + target.p[self.nA + a.id] * (1 - p)
                if score > bestS:
                    bestA = a
                    bestS = score
        return bestA.id if bestA is not None else None

    def submitResult(self, studentID, activityID, result):
        self.count += 1

        if(result == 1):
            self.history[studentID].add(activityID)
        
        ev = E.Event(
            activity=self.activities[activityID],
            student=self.students[studentID],
            result=result,
            counts=list(self.students[studentID].counts)
        )
        self.events.append(ev)
        ev.student.runActivity(ev)
        self.activities[activityID].events.append(ev)

        if(self.count == int(self.nS)):
            self.fit()

    def fit(self):
        for a in self.activities:
            a.fit()

