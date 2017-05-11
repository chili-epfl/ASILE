import random
import numpy as np

import utils

class LFA:
    def __init__(self, id, nA):
        self.id = id
        self.nA = nA
        self.counts = np.array([0. for _ in range(self.nA + 1)])
        self.counts[self.nA] += 1

    def runActivity(self, activity):
        success = random.random() < utils.proba(activity, self.counts)
        self.counts[activity.id] += 1.
        return (1. if success else 0.)

class PFA:
    def __init__(self, id, nA):
        self.id = id
        self.nA = nA
        self.counts = np.array([0. for _ in range(2 * self.nA + 1)])
        self.counts[2 * self.nA] += 1

    def runActivity(self, activity):
        success = random.random() < utils.sigmoid(np.dot(self.count, activity.p))
        self.counts[activity.id + (0 if success else self.nA)] += 1.
        return (1. if success else 0.)
