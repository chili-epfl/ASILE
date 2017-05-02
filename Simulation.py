import random

import Activity as A
import Student as S
import Event as E

class Simulation:

    def __init__(self, config):
        self.config = config

        self.filename = config['filename']

        self.nA = config['numberActivities']
        self.nS = config['numberStudents']
        self.nAS = config['numberOfActivityPerStudent']

        self.activities = [A.Activity(id, self.nA, self.nAS) for id in range(self.nA)]
        self.students = [S.Student(id, self.nA) for id in range(self.nS)]

        self.events = []

    def run(self):
        print('run')

        # makes a shuffled list where every student appears nAcPeSt times
        studentIDs = list(range(self.nS)) * self.nAS
        random.shuffle(studentIDs)

        for id in studentIDs:
            student = self.students[id]
            activity = random.choice(self.activities)
            result = student.runActivity(E.Event(activity, None, None))

            self.events.append({
                's': student.id,
                'a': activity.id,
                'r': result
            })

    def save(self):
        configFile = open('./data/' + self.filename + '_META', 'w')
        configFile.write(str(self.config))
        configFile.close()

        acFile = open('./data/' + self.filename + '_AC', 'w')
        for a in self.activities:
            acFile.write(str({
                'i': a.id,
                'p': a.p
            }) + '\n')
        acFile.close()

        evFile = open('./data/' + self.filename + '_EV', 'w')
        for e in self.events:
            evFile.write(str(e) + '\n')
        evFile.close()
