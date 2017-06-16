import random
import utils
import numpy as np
import multiprocessing

from activity import *
from student import *
from event import *

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
        self.model.events = []
        self.model.students = {}

        for studentID in range(nS):
            # The simulated student performs the activities
            # recommended by the optimizer
            _n = random.choice([nAS-1, nAS, nAS+1])
            for _ in range(_n):
                nextActivityID = optimizer.nextActivity(studentID)
                if nextActivityID is not None:
                    p = self.model.getProba(nextActivityID, studentID)
                    result = 1 if p > random.random() else 0
                    self.model.reportEvent(studentID, nextActivityID, result, None, withState=True)
                    optimizer.submitResult(studentID, nextActivityID, result)
            # The simulated student performs the test activity id=0
            p = self.model.getProba(0, studentID)
            result = 1 if p > random.random() else 0
            optimizer.submitResult(studentID, 0, result)


    def scoreFn(self, e):
        #return 1 if e.activity.id == self.model.optimalChoice(e.state) else 0
        return self.model.evaluateChoice(e.state, e.activity.id)


    def evaluateOptimality(self):
        n = 200
        scores = [ 0. ] * math.ceil(len(self.model.events) / n)
        optScores = [ 0. ] * math.ceil(len(self.model.events) / n)
        for i in range(len(self.model.events)):
            (S, optS) = self.scoreFn(self.model.events[i])
            scores[i // n] += S
            optScores[i // n] += optS
        for i in range(len(scores)):
            scores[i] /= max(1e-4,optScores[i])
        return scores

'''
SimulationLFA
'''

class SimulationLFA(Simulation):

    def __init__(self, nA, model):
        Simulation.__init__(self, nA, model)

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
