import random
import math

import utils

import Activity as A
import Student as S
import Event as E

class Model:

    def __init__(self, config):

        self.filename = config['filename']
        self.nA = config['numberActivities']
        self.nS = config['numberStudents']
        self.nAS = config['numberOfActivityPerStudent']

    def init(self):
        self.activities = [A.Activity(id, self.nA, self.nAS) for id in range(self.nA)]
        self.students = [S.Student(id, self.nA) for id in range(self.nS)]
        self.events = []
        with open('./data/' + self.filename + '_EV') as eventFile:
            for e in [eval(line) for line in eventFile.readlines()]:
                ev = E.Event(
                    self.activities[e['a']],
                    self.students[e['s']],
                    e['r']
                )
                self.events.append(ev)
                
                ev.counts = list(ev.student.counts)
                ev.student.runActivity(ev)

                ev.activity.events.append(ev)

    def fit(self):
        self.init()

        for a in self.activities:
            a.fit()

    def eval(self):
        print('-> EVAL <-')
        for a in self.activities:
            print(a.p)


    def evalReal(self):
        print('-> EVAL REAL <-')

        acFile = open('./data/' + self.filename + '_AC', 'r')
        RealWeights = [ eval(line) for line in acFile.readlines() ]
        acFile.close()

        activities = []
        for id in range(self.nAc):
            activity = A.Activity(id, self.nSk)
            activity.p = RealWeights[id]['p']
            activity.T = RealWeights[id]['T']
            activities.append(activity)

        students = []
        for id in range(self.nSt):
            student = S.Student(id, self.nSk)
            students.append(student)

        events = []
        eventFile = open('./data/' + self.filename + '_EV')
        for id, ev in enumerate([eval(line) for line in eventFile.readlines()]):
            e = E.Event(id,
                activities[ev['a']],
                students[ev['s']],
                ev['r']
            )
            events.append(e)
            students[ev['s']].events.append(e)
            activities[ev['a']].events.append(e)

        for student in students:
            student.getSkillSequence()
        loglikelihood = 0.

        for event in events:
            p = utils.sigmoid(sum(
                [ event.activity.p[k] * event.skillBefore[k] for k in range(self.nSk) ]
            ) + event.activity.p[self.nSk] )
            loglikelihood += math.log((p if event.result else 1 - p))

        print(loglikelihood)
