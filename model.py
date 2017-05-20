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

            event = Event(
                student=self.students[studentID],
                activity=self.activities[activityID],
                result=result,
                date=date,
                state=None
            )

            self.events.append(event)
            self.activities[activityID].events.append(event)
            self.students[studentID].events.append(event)

        for ev in self.events:
            ev.state = ev.student.getState(ev.date)

        #for activity in self.activities.values():
        #    activity.fit()

        pool = multiprocessing.Pool(processes=8)
        for a in pool.map(fit, self.activities.values()):
            self.activities[a.id] = a
        pool.close()
        pool.join()

    def getProba(self, activityID, studentID):
        raise Exception('Parent method not implemented')


'''
ModelLFA
'''


class ModelLFA(Model):

    def __init__(self):

        self.studentModel = StudentLFA
        self.activityModel = ActivityLFA

        self.activities = {}
        self.students = {}

        self.events = []

    def getProba(self, activityID, studentID):
        params = self.activities[activityID].params
        state = self.students[studentID].getState()
        state = [ state.get(i,0) for i in range(len(params) - 1) ] + [ 1 ]
        return 1. / (1. + np.exp(- np.dot(params, state)))

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
