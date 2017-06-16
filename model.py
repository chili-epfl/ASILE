import random
import numpy as np
import multiprocessing

import utils

from activity import *
from student import *
from event import *


'''
Model
'''
def fit(a):
    a.fit()
    return a

class Model:

    def __init__(self):

        self.activities = {}
        self.students = {}

        self.events = []

    def getStudentModel(self, id):
        raise Exception('Parent method not implemented')

    def getActivityModel(self, id):
        raise Exception('Parent method not implemented')

    def runData(self, data):

        for [studentID, activityID, date, result] in data:
            if studentID not in self.students:
                self.students[studentID] = self.getStudentModel(studentID)

            if activityID not in self.activities:
                self.activities[activityID] = self.getActivityModel(activityID)

            self.reportEvent(studentID, activityID, result, date, withState=False)

        for ev in self.events:
            ev.state = ev.student.getState(ev.date)

        self.fit()

    def fit(self):
        pool = multiprocessing.Pool(processes=8)
        for a in pool.map(fit, self.activities.values()):
            self.activities[a.id] = a
        pool.close()
        pool.join()

    def reportEvent(self, studentID, activityID, result, date, withState=False):
        if studentID not in self.students:
            self.students[studentID] = self.getStudentModel(studentID)

        if activityID not in self.activities:
            self.activities[activityID] = self.getActivityModel(activityID)

        event = Event(
            student=self.students[studentID],
            activity=self.activities[activityID],
            result=result,
            date=date,
            state=self.students[studentID].getState(date) if withState else None
        )

        self.events.append(event)
        self.activities[activityID].events.append(event)
        self.students[studentID].events.append(event)

    def optimalChoice(self, state):
        raise Exception('Parent method not implemented')

    def evaluateChoice(self, state, choice):
        raise Exception('Parent method not implemented')

    def getProba(self, activityID, studentID):
        raise Exception('Parent method not implemented')


'''
ModelLFA
'''


class ModelLFA(Model):

    def __init__(self, D):

        Model.__init__(self)

        self.D = D

    def getStudentModel(self, id):
        return StudentLFA(id, self.D)

    def getActivityModel(self, id):
        return ActivityLFA(id, self.D)

    def getProba(self, activityID, studentID):
        if studentID not in self.students:
            self.students[studentID] = self.getStudentModel(studentID)

        if activityID not in self.activities:
            self.activities[activityID] = self.getActivityModel(activityID)

        params = self.activities[activityID].params
        state = self.students[studentID].getState(None)
        state = [ state.get(a,0) for a in range(self.activities[activityID].D) ] + [ 1 ]
        return 1. / (1. + np.exp(- np.dot(params, state)))

    def optimalChoice(self, state):
        optActivity = None
        optScore = -10.

        available = [a for a in self.activities.values() if a.id not in state.keys()]
        for activity in available:
            score = self.activities[0].params[activity.id]
            if score > optScore:
                optScore = score
                optActivity = activity.id

        return optActivity

    def evaluateChoice(self, state, choice):
        optChoice = self.optimalChoice(state)
        optS = max(1e-3, self.activities[0].params[optChoice])
        S = max(1e-3, self.activities[0].params[choice])
        # print()
        # print('STATE', state)
        # print('OPTIM', optChoice, optS, 'CHOICE', choice, S)
        # print()
        return (S, optS)

'''
    def init(self, events):
        self.activities = [ActivityLFA(id, self.nA) for id in range(self.nA)]
        self.events = []
        for e in events:
            ev = Event(
                activity=self.activities[e.activity.id],
                result=e.result,
                counts=np.copy(e.counts)
            )
            self.events.append(ev)
            ev.activity.events.append(ev)

    def fit(self, events=None):
        if events is not None:
            self.init(events)
        for a in self.activities:
            a.fit()
'''
