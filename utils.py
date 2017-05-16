import numpy as np
import sys, os

DEBUG = False

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def sigmoid(x):
    return 1. / (1. + np.exp(-x))

def optimal(model, target, counts):
    bestS = 0.
    bestA = target
    for a in model.activities:
        if counts[a.id] < 1:
            score = target.p[a.id]
            if score > bestS:
                bestA = a
                bestS = score
    return bestS, bestA.id


def eval(n, model, sim, events):
    score = 0.
    for e in events:
        pm = proba(model.activities[e.activity.id], e.counts)
        ps = proba(sim.activities[e.activity.id], e.counts)
        score += (pm - ps) ** 2.
    score = (score / len(events)) ** 0.5
    return score


def proba(activity, counts):
    return (sigmoid(np.dot(activity.p, counts)))
