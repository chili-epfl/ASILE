import random
import math
from sklearn import linear_model
import statsmodels.discrete.discrete_model as sm
import numpy as np

import utils

class Activity:

    def __init__(self, id, nA):
        self.id = id
        self.nA = nA
        self.p = [ random.random() for _ in range(self.nA * 2 )] + [ - random.random() * self.nA / 4]
        self.events = []

    def fit(self):
        X = []
        y = []
        for e in self.events:
            X.append(e.counts + [ 1 ])
            y.append(e.result)
        X.append([ 0.1 * random.random() for _ in range(self.nA * 2)] + [ 1 ])
        y.append(0.)
        X.append([ 1 - 0.1 * random.random() for _ in range(self.nA * 2)] + [ 1 ])
        y.append(1.)


        #print(len(X))
        #print(X)
        #rank = np.linalg.matrix_rank(X)
        #print(rank)
        #if(rank < 2 * self.nA + 1):
            #for _ in range(self.nA + 1 - rank // 2):
                #X.append([ 0.1 * random.random() for _ in range(self.nA * 2)] + [ 1 + 0.1 * random.random() ])
                #y.append(0.)
                #X.append([ 0.1 * random.random() for _ in range(self.nA * 2)] + [ 1 + 0.1 * random.random() ])
                #y.append(1.)
        
        #print(np.linalg.matrix_rank(X))

        #LR = linear_model.LogisticRegression(solver='liblinear', fit_intercept=False)
        #LR.fit(X,y)
        #self.p = LR.coef_[0]
        #print(LR.coef_[0])

        logit = sm.Logit(y, X)
        result = logit.fit_regularized(disp=False, method='l1')
        self.p = result.params
        self.e = result.bse
