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
        self.studentModel = None
        self.activityModel = None

        self.activities = {}
        self.students = {}

        self.events = []

    def fit(self, data):
        for [studentID, activityID, date, result] in data:

            if studentID not in self.students:
                self.students[studentID] = self.studentModel(studentID)

            if activityID not in self.activities:
                self.activities[activityID] = self.activityModel(activityID)

            self.reportEvent(studentID, activityID, result, date)

        for ev in self.events:
            ev.state = ev.student.getState(ev.date)

        #for activity in self.activities.values():
        #    activity.fit()

        pool = multiprocessing.Pool(processes=8)
        for a in pool.map(fit, self.activities.values()):
            self.activities[a.id] = a
        pool.close()
        pool.join()

    def reportEvent(self, studentID, activityID, result, date, withState=False):
        event = Event(
            student=self.students[studentID],
            activity=self.activities[activityID],
            result=result,
            date=date,
            state=self.students[studentID].getState(None) if withState else None
        )

        self.events.append(event)
        self.activities[activityID].events.append(event)
        self.students[studentID].events.append(event)

    def optimalChoice(self, state):
        raise Exception('Parent method not implemented')

    def getProba(self, activityID, studentID):
        raise Exception('Parent method not implemented')


'''
ModelLFA
'''


class ModelLFA(Model):

    def __init__(self):

        Model.__init__(self)

        self.studentModel = StudentLFA
        self.activityModel = ActivityLFA

    def getProba(self, activityID, studentID):
        if studentID not in self.students:
            self.students[studentID] = self.studentModel(studentID)

        if activityID not in self.activities:
            self.activities[activityID] = self.activityModel(activityID)

        params = self.activities[activityID].params
        state = self.students[studentID].getState(None)
        state = [ state.get(a,0) for a in self.activities[activityID].activityList ] + [ 1 ]
        return 1. / (1. + np.exp(- np.dot(params, state)))

    def optimalChoice(self, state):
        optActivity = None
        optScore = 0.

        available = [a for a in self.activities.values() if a.id not in state.keys()]

        for activity in available:
            score = 0.
            for a in self.activities.values():
                updatedState = [ 1 if i == activity.id else state.get(i,0) for i in a.activityList ] + [ 1 ]
                score += 1. / (1. + np.exp(- np.dot(a.params, updatedState)))
            if score > optScore:
                optScore = score
                optActivity = activity.id

        return optActivity

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
