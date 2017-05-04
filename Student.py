import random

import utils

class Student:

    def __init__(self, id, nA):
        self.id = id
        self.nA = nA
        self.counts = [0. for _ in range(self.nA * 2)]

    def runActivity(self, event):
        result = event.result
        if result is None:
            result = 1. if random.random() < utils.sigmoid(sum(
                [ event.activity.p[k] * self.counts[k] for k in range(len(self.counts)) ]
            ) + event.activity.p[self.nA * 2]) else 0.
        self.counts[event.activity.id + (self.nA if result == 1. else 0)] += 1.
        return result
