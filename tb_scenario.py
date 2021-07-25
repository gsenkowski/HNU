import scenario
import numpy as np

#Two Body Scenario
class TBScenario(scenario.Scenario):
    def __init__(self, position1, velocity1, mass1, position2, velocity2, mass2, gms1=None, gms2=None):
        self.masses = np.asarray((mass1, mass2))
        self.positions = np.asarray((position1, position2))
        self.velocities = np.asarray((velocity1, velocity2))
        if gms1 != None and gms2 != None:
            self.gms = np.asarray((gms1, gms2))
        else:
            self.gms = None

    def get_masses(self):
        return self.masses

    def get_velocities(self):
        return self.velocities

    def get_positions(self):
        return self.positions

    def get_gms(self):
        if self.gms is None:
            return self.masses * 6.67408E-11
        else:
            return self.gms

    def get_ids(self):
        return('0', '1')
    