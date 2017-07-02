import random
import utils
import numpy as np
import multiprocessing

from activity import *
from student import *
from event import *
from model import *

'''
Simulation
'''

class Simulation:
    def __init__(self, nA, model):
        self.nA = nA
        self.model = model

    def run(self, nS=100, interactions=1000, filename='SIM'):
        raise Exception('Parent method not implemented')

    def runWithOptimizer(self, optimizer, nAS, nS):
        self.success = 0
        self.failure = 0

        self.optimizerChoices = {}
        self.model.events = []
        self.model.students = {}
        self.nS = nS

        for studentID in range(nS):
            self.optimizerChoices[studentID] = []

            # The simulated student performs the activities
            # recommended by the optimizer
            _n = nAS
            for _ in range(_n):
                nextActivityID = optimizer.nextActivity(studentID)
                if nextActivityID is not None:
                    self.optimizerChoices[studentID].append(nextActivityID)
                    p = self.model.getProba(nextActivityID, studentID)
                    result = 1 if p > random.random() else 0
                    self.model.reportEvent(studentID, nextActivityID, result, None, withState=True)
                    optimizer.submitResult(studentID, nextActivityID, result)

            # The simulated student performs the test activity id=0
            p = self.model.getProba(0, studentID)
            result = 1 if p > random.random() else 0
            optimizer.submitResult(studentID, 0, result)
            if result:
                self.success += 1
            else:
                self.failure += 1


    def scoreFn(self, choices):
        #return 1 if e.activity.id == self.model.optimalChoice(e.state) else 0
        return self.model.evaluateChoices(choices)


    def evaluateOptimality(self):
        n = self.nS // 50
        scores = [ 0. ] * self.nS
        optScores = [ 0. ] * self.nS
        for studentID in range(self.nS):
            (S, optS) = self.scoreFn(self.optimizerChoices[studentID])
            scores[studentID] = S
            optScores[studentID] = optS
        res = [ 0 ] * (len(scores))
        for i in range(len(scores)):
            res[i] = sum(scores[i:(i+n)]) / max(1e-4,sum(optScores[i:(i+n)]))
        return res, self.success, self.failure

'''
SimulationLFA
'''

class SimulationLFA(Simulation):

    def __init__(self, nA, model):
        self.nA = nA
        self.model = ModelLFA(nA)
        for id in range(nA):
            a = ActivityLFA(id, nA)
            a.params = list(model.activities[id].params[0:nA]) + [ model.activities[id].params[-1] ]
            self.model.activities[id] = a

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
            self.model.events.append(Event(
                activity=activity,
                student=student,
                result=result,
                counts=counts
            ))
