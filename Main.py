import Simulation
import Model
import Optimizer

CONFIG = {
    'filename': 'SIM',

    'numberStudents': 10000,
    'numberActivities': 10,

    'numberOfActivityPerStudent': 18
}

o = Optimizer.Optimizer()
o.run()

