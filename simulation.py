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
            for _ in range(nAS):
                nextActivityID = optimizer.nextActivity(studentID)

                if nextActivityID is not None:
                    p = self.model.getProba(nextActivityID, studentID)
                    result = 1 if p > random.random() else 0
                    self.model.reportEvent(studentID, nextActivityID, result, None, withState=True)
                    optimizer.submitResult(studentID, nextActivityID, result)


    def scoreFn(self, e):
        return 1 if e.activity.id == sim.model.optimalChoice(e.state) else 0

    def evaluateOptimality(self):

        pool = multiprocessing.Pool(processes=8)
        score = sum(pool.map(self.scoreFn, self.model.events))
        pool.close()
        pool.join()

        score /= len(self.model.events)
        return score

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
