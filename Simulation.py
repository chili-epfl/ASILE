import random
import utils
import numpy as np

import Activity
import Student
import Event

class Simulation:
    def __init__(self, nA=8):
        self.nA = nA
        self.activities = [Activity.LFA(id, self.nA) for id in range(self.nA)]

    def run(self, nS=100, interactions=1000, filename='SIM'):
        self.events = []
        self.students = [Student.LFA(id, self.nA) for id in range(nS)]

        studentIDs = list(range(nS))
        random.shuffle(studentIDs)

        for _ in range(interactions):
            student = random.choice(self.students)
            activity = random.choice(self.activities)

            counts = np.copy(student.counts)
            result = student.runActivity(activity)
            self.events.append(Event.Event(
                activity=activity,
                student=student,
                result=result,
                counts=counts
            ))

    def runWithOptimizer(self, optimizer, nAS, nS):
        self.events = []
        self.students = [S.Student(id, self.nA) for id in range(nS)]

        for student in self.students:
            for _ in range(nAS):
                nextA = optimizer.nextActivity(student.id)
                if nextA is not None:
                    activity = self.activities[nextA]

                    counts = list(student.counts)
                    result = student.runActivity(E.Event(activity, None, None))
                    self.events.append(E.Event(
                        activity=activity,
                        student=student,
                        result=result,
                        counts=counts
                    ))
                    optimizer.submitResult(student.id, activity.id, result)

    def evaluateOptimality(self):
        score = 0.
        for e in self.events:
            p = utils.proba(e.activity, e.counts)
            s = self.activities[0].p[e.activity.id] * p + self.activities[0].p[self.nA + e.activity.id] * (1 -p)
            bestS, bestA = utils.optimal(self, self.activities[0], e.counts)
            score += s / bestS
            #score += 1 if e.activity.id == utils.optimal(self, self.activities[0], e.counts) else 0

        score /= len(self.events)
        print('OPTIMALITY SCORE:', score)
        return score
