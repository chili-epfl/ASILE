import sys, os

import pymoocdb

import pandas as pd
import numpy as np
import networkx as nx
import math

DEBUG = False


'''
Allows to disable print on stdout
'''


STDOUT = sys.stdout


def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = STDOUT

'''
Utils
'''

def getSQLData(subset):

    SQLQuery = """
    SELECT DISTINCT
        EPFL_HashedSciper,
        EPFL_CourseID,
        EPFL_ExamDate,
        EPFL_EPFLCourseGrade
    FROM semester_projects.epfl_and_mooc_grades
    LIMIT 100000;
    """

    db = pymoocdb.MoocDBLink()
    db.ExecuteQuery(SQLQuery)
    db.close()

    data = pd.DataFrame(
        data=db.GetReturnedRows(),
        columns=['StudentID', 'CourseID', 'ExamDate', 'Grade']
    )
    data.Grade = data.Grade.apply(pd.to_numeric, errors='coerce')
    data.ExamDate = data.ExamDate.apply(pd.to_datetime)
    data.CourseID = data.CourseID.apply(lambda x: x.split('(')[0])
    data = data[data.CourseID.isin(subset)]
    data.dropna(axis=0, inplace=True)

    def z(obj, key):
        if key not in obj:
            obj[key] = len(obj)
        return obj[key]

    _students = {}
    _courses = {}

    data.StudentID = data.StudentID.apply(lambda x: z(_students, x))
    data.CourseID = data.CourseID.apply(lambda x: z(_courses, x))

    courses = {v: k for k,v in _courses.items()}

    data['Result'] = data.Grade.apply(lambda grade: 1 if grade > 3.9 else 0)
    data.sort_values(by='ExamDate', inplace=True)
    data.reset_index(drop=True, inplace=True)

    return (data, courses)

def generateGraph(name, activities, labels, thickness, color):
    r = 5
    def POSITION(n={ 'n': 0 }):
        x = math.cos(((math.pi * 2) / len(activities)) * n['n']) * r
        y = math.sin(((math.pi * 2) / len(activities)) * n['n']) * r
        n['n'] += 1
        return '\"' + str(x) + ',' + str(y) + '!\"'

    NODE_SIZE_SCALE = lambda x: max(5e-2 * (x ** 0.5), 1.2e0)

    G = nx.DiGraph()

    G.add_nodes_from([ (a.id, {
        'label': labels[a.id],
        'fixedsize': 'true',
        'fontsize': 14 * NODE_SIZE_SCALE(len(a.events)) / NODE_SIZE_SCALE(0),
        'pos': POSITION(),
        'width': NODE_SIZE_SCALE(len(a.events)),
        'shape': 'circle',
        'fillcolor': color,
        'penwidth': 3,
        'style': 'filled'
    }) for a in activities ])

    for a in activities:
        for b in range(a.D):
            if b != a.id:
                t = thickness(a, b)
                if t > 0.5 and a.counts[b] > 50:
                    G.add_edge(b, a.id, {
                        'penwidth': t
                    })
    nx.drawing.nx_pydot.write_dot(G, name + '.dot')
    os.system('neato -Tpng ' + name + '.dot -o ' + name + '.png')

'''
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
'''
