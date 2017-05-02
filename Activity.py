import random
import math
from sklearn import linear_model

import utils

class Activity:

    def __init__(self, id, nA, nAS):
        self.id = id
        self.nA = nA
        self.p = [random.random() for _ in range(self.nA)] + [ - random.random() * nAS / 2 ]
        self.events = []

    def fit(self):
        X = []
        y = []

        for e in self.events:
            X.append(e.counts + [ 1. ])
            y.append(e.result)

        LR = linear_model.LogisticRegression()
        LR.fit(X,y)

        self.p = LR.coef_[0]
