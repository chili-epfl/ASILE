import random
import numpy as np

import utils

import Activity
import Student
import Event

class Model:

    def __init__(self, nA=8):
        self.activities = []
        self.students = []
        self.events = []
        self.nA = nA

    def init(self, events):
        self.activities = [Activity.LFA(id, self.nA) for id in range(self.nA)]
        self.events = []
        for e in events:
            ev = Event.Event(
                activity= self.activities[e.activity.id],
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
