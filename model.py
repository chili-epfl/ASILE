import random
import numpy as np

import utils

from activity import *
from student import *
from event import *


'''
Model
'''


class Model:

    def __init__(self, nA=10):
        self.activities = []
        self.students = []
        self.events = []
        self.nA = nA

    def init(self, events):
        raise Exception('Parent method not implemented')

    def fit(self, events=None):
        raise Exception('Parent method not implemented')


'''
ModelLFA
'''


class ModelLFA:

    def __init__(self, nA=8):
        self.activities = []
        self.students = []
        self.events = []
        self.nA = nA

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
