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

    def __init__(self, id, nA):
        self.id = id

    def getProba(self, studentState):
        raise Exception('Parent method not implemented')


'''
ActivityLFA
'''


class ActivityLFA(Activity):
    def __init__(self, id, nA):
        self.id = id
        self.nA = nA
        self.p = np.array([random.random() for _ in range(self.nA + 1)])
        self.p[self.nA] = - random.random() * self.nA / 3
        self.e = np.array([100. for _ in range(self.nA + 1)])
        self.events = []

    def getProba(self, studentState):
        return 1. / (1. + np.exp(-np.dot(self.p, studentState)))

    def fit(self):
        X = [e.counts for e in self.events]
        y = [e.result for e in self.events]


        if not utils.DEBUG:
            utils.blockPrint()

        try:
            # LR = linear_model.LogisticRegression(
            #    solver='liblinear',
            #    fit_intercept=False
            # )
            # LR.fit(X,y)
            # self.p = LR.coef_[0]

            logit = sm.Logit(y, X)
            result = logit.fit_regularized(
                start_params=self.p,
                disp=0,
                qc_verbose=0,
                method='l1',
                alpha=1e-2)
            self.p = np.array(result.params)
            self.e = np.array(result.bse)

        except Exception as err:
            print('Exception:', err)

        utils.enablePrint()
