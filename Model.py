import random

import utils

import Activity as A
import Student as S
import Event as E

class Model:

    def __init__(self, nA=10):
        self.activities = []
        self.students = []
        self.events = []
        self.nA = nA

    def init(self, nS, events):
        self.activities = [A.Activity(id, self.nA) for id in range(self.nA)]
        self.students = [S.Student(id, self.nA) for id in range(nS)]
        self.events = []
        for e in events:
            ev = E.Event(
                activity=self.activities[e.activity.id],
                student=self.students[e.student.id],
                result=e.result
            )
            self.events.append(ev)
            ev.counts = list(ev.student.counts)
            ev.student.runActivity(ev)
            ev.activity.events.append(ev)

    def fit(self, nS=100, events=[]):
        self.init(nS, events)
        for a in self.activities:
            a.fit()

