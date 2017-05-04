import random

import Activity as A
import Student as S
import Event as E

class Simulation:

    def __init__(self, filename='SIM', nA=10):
        self.filename = filename
        self.nA = nA
        self.activities = [A.Activity(id, self.nA) for id in range(self.nA)]

    def run(self, nS=100, nAS=5, filename='SIM'):
        self.events = []
        self.students = [S.Student(id, self.nA) for id in range(nS)]
        
        studentIDs = list(range(nS)) * nAS
        random.shuffle(studentIDs)
        
        for id in studentIDs:
            student = self.students[id]
            counts = list(student.counts)
            activity = random.choice(self.activities)
            result = student.runActivity(E.Event(activity, None, None))
            self.events.append(E.Event(
                activity=activity, 
                student=student, 
                result=result,
                counts=counts
            ))
