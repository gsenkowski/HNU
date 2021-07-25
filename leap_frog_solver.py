
from solver import Solver
from hss_scenario import HSSScenario
import numpy as np
from numba import njit, prange
import datetime
import math
import time
from com_evaluator import COM_Evaluator
from am_evaluator import AM_Evaluator
from energy_evaluator import Energy_Evaluator
from rel_distance_evaluator import Rel_Distance_Evaluator
from rel_velocity_evaluator import Rel_Velocity_Evaluator

@njit()
def compute(gms, positions, velocities, duration, stepsize):
    forces = np.zeros((len(gms), len(gms), 3), dtype=np.float64)
    bodycount = len(gms)

    positions = positions + stepsize * 0.5 * velocities

    for step in range(int(duration / stepsize) - 1):
        if step % int(24 * 60 * 60 / stepsize) == 0:
            print('day passed')
        for body1 in range(bodycount):
            for body2 in range(bodycount):
                if body1 != body2:
                    distance = positions[body2] - positions[body1]
                    #forces[body1][body2] = G * ((masses[body1] * masses[body2]) / (np.linalg.norm(distance) ** 3)) * distance

                    forces[body1][body2] = gms[body2] * distance / (math.sqrt(distance[0] ** 2 + distance[1] ** 2 + distance[2] ** 2) ** 3)

        acceleration = np.sum(forces, axis=1)
        velocities = velocities + stepsize * acceleration
        positions = positions + stepsize * velocities
    positions = positions + stepsize * 0.5 * velocities




    return positions, velocities


class LeapFrog(Solver):

    def __init__(self):
        self.scenario = None



    def solve(self, duration, stepsize):
        if self.scenario is None:
            return 1
        gms = self.scenario.get_gms()

        positions = self.scenario.get_positions()
        velocities = self.scenario.get_velocities()

        before = time.time()
        result = compute(gms, positions, velocities, duration, stepsize)
        after = time.time()
        print('Complete after ' + str(after - before) + 'seconds')
        return result


    def set_scenario(self, scenario):
        self.scenario = scenario


def main():

    # Create start and end date
    date1 = datetime.datetime(2021, 6, 23, 12, 00, 00)
    date2 = datetime.datetime(2022, 6, 23, 12, 00, 00)
    # Create Scenario
    scen = HSSScenario(date1)
    # Create Solver
    test_solver = LeapFrog()
    # set scenario for solver
    test_solver.set_scenario(scen)
    time_difference = (date2 - date1)
    positions, velocities = test_solver.solve(int(time_difference.total_seconds()), 25)
    print((time_difference.total_seconds()) / (24 * 60 * 60))

    scen2 = HSSScenario(date2)


    rel_dist_eval = Rel_Distance_Evaluator()
    rel_dist = rel_dist_eval.evaluate(scen2, positions, velocities)

    for Id in ('10', '199', '299', '399', '499', '599', '699', '799', '899', '999'):
        print('Body ' + Id + ' difference in position: ' + str(rel_dist[Id]) + 'seconds')
    print('')

    rel_vel_eval = Rel_Velocity_Evaluator()
    rel_vel = rel_vel_eval.evaluate(scen2, positions, velocities)

    for Id in ('10', '199', '299', '399', '499', '599', '699', '799', '899', '999'):
        print('Body ' + Id + ' difference in velocity: ' + str(rel_vel[Id]))
    print('')


    com_eval = COM_Evaluator()
    com = com_eval.evaluate(scen,positions,velocities, 365*24*60*60)
    print(com)

    am_eval = AM_Evaluator()
    am = am_eval.evaluate(scen,positions,velocities)
    print(am)

    e_eval = Energy_Evaluator()
    energy = e_eval.evaluate(scen,positions,velocities)
    print(energy)
if __name__ == "__main__":
    # execute only if run as a script
    main()