from simulation import *
from model import *
from optimizer import *

import numpy as np
import utils

'''
Configuration
'''


nA = 5
nS = 1000
nAS = 5


'''
Core of the program
'''


s = SimulationLFA(nA=nA)
m = ModelLFA(nA=nA)

for a in s.activities[:5]:
    print('ACTIVITY', a.id, a.p)
s.run(nS=1000, interactions=int(0.8 * nA * 1000))
testEvents = list(s.events)



def test(nStudent, model, sim):
    print('\n>>>>>>>>>>\n>>>>>>>>>>\n')
    print('TEST=', nStudent)

    print('simulating . . .')
    sim.run(nS=nStudent, interactions=int(0.8 * nA * nStudent))

    print('fitting . . .')
    model.fit(events=sim.events)

    for a in model.activities[:2]:
        print('ACTIVITY', a.id, a.p)

    print('evaluating . . .')
    print('SCORE=', utils.eval(nStudent, model, sim, testEvents))


test(10, m, s)
test(100, m, s)
test(300, m, s)
test(1000, m, s)
test(3000, m, s)
test(10000, m, s)


results = {
    'random': [],
    'epsilon': [],
    'bandit': []
}

for i in range(1):
    print('\n')
    print('ITERATION', i, '\n')
    s = SimulationLFA(nA=nA)

    print('>>>>>>>>>>', 'RANDOM')
    o = RandomOptimizer(nA=nA)
    s.runWithOptimizer(o, nAS, nS)
    results['random'].append(s.evaluateOptimality())

    print('>>>>>>>>>>', 'EPSILON')
    o = EpsilonOptimizer(nA=nA)
    s.runWithOptimizer(o, nAS, nS)
    results['epsilon'].append(s.evaluateOptimality())

    print('>>>>>>>>>>', 'BANDIT')
    o = BanditOptimizer(nA=nA)
    s.runWithOptimizer(o, nAS, nS)
    results['bandit'].append(s.evaluateOptimality())

    print('>>>>>>>>>>')

print('\n\n>>>>>>>>>>\n>>>>>>>>>>\n>>>>>>>>>>\n\n\n')

print('STUDENTS', nS)
print('RANDOM', np.mean(results['random']), np.std(results['random']))
print('EPSILO', np.mean(results['epsilon']), np.std(results['epsilon']))
print('BANDIT', np.mean(results['bandit']), np.std(results['bandit']))

print('\n>>>>>>>>>>\n>>>>>>>>>>\n')
