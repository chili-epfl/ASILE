import random
import math
from sklearn import linear_model
import statsmodels.discrete.discrete_model as sm
import numpy as np

import utils

class LFA:
    def __init__(self, id, nA):
        self.id = id
        self.nA = nA
        self.p = np.array([ 3 * (random.random() ** 2) for _ in range(self.nA)] + [ - random.random() * self.nA ])
        self.events = []

    def fit(self):
        X = []
        y = []
        for e in self.events:
            X.append(e.counts)
            y.append(e.result)
        X.append([ 0.1 * random.random() for _ in range(self.nA)] + [ 1 + 0.1 * random.random() ])
        y.append(0.)
        X.append([ 1 - 0.1 * random.random() for _ in range(self.nA)] + [ 1 + 0.1 * random.random() ])
        y.append(1.)

        #print(len(X))
        #print(X)
        #rank = np.linalg.matrix_rank(X)
        #print(rank)
        #if(rank < self.nA + 1):
            #for _ in range(self.nA + 1 - rank // 2):
                #X.append([ 0.1 * random.random() for _ in range(self.nA)] + [ 1 + 0.1 * random.random() ])
                #y.append(0.)
                #X.append([ 0.1 * random.random() for _ in range(self.nA)] + [ 1 + 0.1 * random.random() ])
                #y.append(1.)

        #print(np.linalg.matrix_rank(X))

        #LR = linear_model.LogisticRegression(solver='liblinear', fit_intercept=False)
        #LR.fit(X,y)
        #self.p = LR.coef_[0]

        if(0. in y and 1. in y):
            logit = sm.Logit(y, X)
            result = logit.fit_regularized(disp=False, method='l1', alpha=1e-2)
            self.p = np.array(result.params)
            self.e = np.array(result.bse)
        else:
            self.p = np.array([0. for _ in range(self.nA + 1)])
            self.e = np.array([100. for _ in range(self.nA + 1)])


class PFA:
    def __init__(self, id, nA):
        self.id = id
        self.nA = nA
        self.p = np.array([ 3 * (random.random() ** 2) for _ in range(2 * self.nA)] + [ - random.random() * self.nA ])
        self.events = []

    def fit(self):
        X = []
        y = []
        for e in self.events:
            X.append(e.counts + [ 1 ])
            y.append(e.result)

        logit = sm.Logit(y, X)
        result = logit.fit_regularized(disp=False, method='l1', alpha=1.)
        self.p = np.array(result.params)
        self.e = np.array(result.bse)
