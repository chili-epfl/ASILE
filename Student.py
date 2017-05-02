import random
import math

import utils

class Student:

    def __init__(self, id, nA):
        self.id = id
        self.nA = nA
        self.counts = [0. for _ in range(self.nA)]

    def runActivity(self, event):
        
        if self.id == 5:
            print(self.id, self.counts, event.activity.id)

        result = event.result
        
        if result is None:
            result = 1. if random.random() < utils.sigmoid(sum(
                [ event.activity.p[k] * self.counts[k] for k in range(self.nA) ]
            ) + event.activity.p[self.nA]) else 0.

        self.counts[event.activity.id] += 1.
                
        if self.id == 5:
            print(self.counts)

        return result
