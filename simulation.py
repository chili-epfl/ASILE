import random
import utils
import numpy as np

from activity import *
from student import *
from event import *

'''
Simulation
'''


class Simulation:
    def __init__(self, nA=8):
        self.nA = nA

    def run(self, nS=100, interactions=1000, filename='SIM'):
        raise Exception('Parent method not implemented')

    def runWithOptimizer(self, optimizer, nAS, nS):
        raise Exception('Parent method not implemented')

    def evaluateOptimality(self, n=0):
        raise Exception('Parent method not implemented')

'''
SimulationLFA
'''


class SimulationLFA(Simulation):
    def __init__(self, nA=8):
        self.nA = nA
        self.activities = [ActivityLFA(id) for id in range(self.nA)]

    def run(self, nS=100, interactions=1000, filename='SIM'):
        self.events = []
        self.students = [StudentLFA(id) for id in range(nS)]

        studentIDs = list(range(nS))
        random.shuffle(studentIDs)

        for _ in range(interactions):
            student = random.choice(self.students)
            activity = random.choice(self.activities)

            counts = np.copy(student.counts)
            result = student.runActivity(activity)
            self.events.append(Event(
                activity=activity,
                student=student,
                result=result,
                counts=counts
            ))

    def runWithOptimizer(self, optimizer, nAS, nS):
        self.events = []
        self.students = [StudentLFA(id, self.nA) for id in range(nS)]

        for student in self.students:
            for _ in range(nAS):
                nextA = optimizer.nextActivity(student.id)
                if nextA is not None:
                    activity = self.activities[nextA]
                    counts = np.copy(student.counts)
                    result = student.runActivity(activity)
                    self.events.append(Event(
                        activity=activity,
                        student=student,
                        result=result,
                        counts=counts
                    ))
                    optimizer.submitResult(student.id, activity.id, result)

    def evaluateOptimality(self, n=0):
        score = 0.
        evs = self.events if n == 0 else self.events[-n:]
        for e in evs:
            s = self.activities[0].p[e.activity.id]

            bestS, bestA = utils.optimal(self, self.activities[0], e.counts)

            score += s / bestS

        score /= len(evs)
        print('OPTIMALITY SCORE:', score)
        return score
