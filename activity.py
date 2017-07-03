import random
import math
from sklearn import linear_model
import statsmodels.discrete.discrete_model as sm
import numpy as np

import utils

'''
Activity
'''


class Activity:

    def __init__(self, id):
        self.id = id


'''
ActivityLFA
'''


class ActivityLFA(Activity):
    def __init__(self, id, D):
        self.id = id
        self.D = D

        self.params = np.array([ 0. ] * (self.D + 1))
        self.counts = np.array([ 0. ] * self.D)
        self.events = []

    def fit(self):
        self.counts = np.array([ 0. ] * self.D)
        for e in self.events:
            for a in e.state:
                self.counts[a] += 1

        X = [
            [ e.state.get(a, 0) if a != self.id else 0 for a in range(self.D) ] + [ 1 ]
            for e in self.events
        ]
        y = [e.result for e in self.events]
        if not 0 in y:
            y.append(0)
            X.append([0 for _ in range(self.D + 1)])
        if not 1 in y:
            y.append(1)
            X.append([1 for _ in range(self.D + 1)])

        try :
            LR = linear_model.LogisticRegression(
                solver='liblinear',
                fit_intercept=False,
                warm_start=True,
                C=5
            )
            LR.fit(X,y)
            self.params = LR.coef_[0]
            self.error = [10. for _ in self.params]
        except Exception as err:
            print('Exception:', err)
