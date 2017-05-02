import Simulation
import Model

CONFIG = {
    'filename': 'SIM_1',

    'numberStudents': 10000,
    'numberActivities': 10,

    'numberOfActivityPerStudent': 18
}

s = Simulation.Simulation(CONFIG)

s.run()
s.save()

m = Model.Model(CONFIG)

m.fit()
m.eval()
