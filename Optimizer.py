import random

import utils

import Simulation
import Model

import Activity as A
import Student as S
import Event as E

nA = 10

class Optimizer:

    def __init__(self):
        pass

    def run(self):


        s = Simulation.Simulation(nA=nA)
        for a in s.activities[:2]:
            print('ACTIVITY', a.id, a.p)

        m = Model.Model(nA=nA)

        optimal(s, s.activities[0], [0. for _ in range(nA * 2) ])
        
        test(10, m, s)
        test(100, m, s)
        test(1000, m, s)
        test(10000, m, s)
        test(100000, m, s)

        print('>>>>>>>>>>\n>>00>>00>>\n>>>>__>>>>\n>>>>>>>>>>')

################################################
################################################
################################################
def optimal(model, target, counts):
    print('>>>>>>>>>>')
    bestS = 0.
    bestA = target
    for a in model.activities:
        if counts[a.id] < 1:
            p = proba(a, counts)
            score = target.p[a.id] * p + target.p[model.nA + a.id] * (1 -p)
            if score > bestS:
                bestA = a
                bestS = score
    print('OPTIMAL:', bestS, bestA.id)

def test(n, model, sim):
    print('>>>>>>>>>>\n>>>>>>>>>>')
    print('simulating . . .')
    sim.run(nS=n, nAS=5)
    print('fitting . . .')
    model.fit(nS=n, events=sim.events)
    for a in model.activities[:2]:
        print('ACTIVITY', a.id, a.p)
    eval(n, model, sim)
    optimal(model, model.activities[0], [0. for _ in range(nA * 2) ])

def eval(n, model, sim):
    print('>>>>>>>>>>')
    print('TEST=', n)

    sim.run(nS=1000, nAS=5, filename='EVAL')
    score = 0.
    for e in sim.events:
        pm = proba(model.activities[e.activity.id], e.counts)
        ps = proba(e.activity, e.counts)
        score += (pm - ps) ** 2.
    score = (score / len(sim.events)) ** 0.5

    print('SCORE=', score)

def proba(activity, counts):
    return (utils.sigmoid(sum(
        [ activity.p[k] * counts[k] for k in range(len(counts)) ]
    ) + activity.p[len(counts)]))