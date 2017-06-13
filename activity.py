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
        self.error = np.array([ 10. ] * (self.D + 1))
        self.counts = np.array([ 0. ] * self.D)
        self.events = []

    def __str__(self):
        return str({
            'id': self.id,
            'p': self.params,
            'e': self.error
        })

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

        if not utils.DEBUG:
            utils.blockPrint()

        try:
            logit = sm.Logit(y, X)
            result = logit.fit_regularized(
                #start_params=self.params,
                disp=0,
                qc_verbose=0,
                method='l1',
                alpha=1e-2)
            self.params = np.array(result.params)
            self.error = np.array(result.bse)

        except Exception as err:
            print('Exception:', err)
            try :
                LR = linear_model.LogisticRegression(
                    solver='liblinear',
                    fit_intercept=False
                )
                LR.fit(X,y)
                self.params = LR.coef_[0]
                self.error = [10. for _ in self.params]
            except Exception as err:
                print('Exception:', err)

        finally:
            utils.enablePrint()
