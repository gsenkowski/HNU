
from solver import Solver
from hss_scenario import HSSScenario
from h_planets_scenario import HPlanetsScenario
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
    accelerations = np.zeros((len(gms), len(gms), 3), dtype=np.float64)
    derivates_accelerations = np.zeros((len(gms), len(gms), 3), dtype=np.float64)

    accelerations_pred = np.zeros((len(gms), len(gms), 3), dtype=np.float64)
    derivates_accelerations_pred = np.zeros((len(gms), len(gms), 3), dtype=np.float64)

    bodycount = len(gms)

    time = duration
    count = 0
    while True:
        if time < stepsize:
            stepsize = time
        if count % int(24 * 60 * 60 / stepsize) == 0:
            print('day passed')
        for body1 in range(bodycount):
            for body2 in range(bodycount):
                if body1 != body2:
                    distance = positions[body2] - positions[body1]
                    rel_vel = velocities[body2] - velocities[body1]
                    abs_distance = math.sqrt(distance[0] ** 2 + distance[1] ** 2 + distance[2] ** 2)
                    accelerations[body1][body2] = gms[body2] * distance / (abs_distance ** 3)
                    derivates_accelerations[body1][body2] = gms[body2] * (
                        (rel_vel/(abs_distance ** 3))
                        - 3 * (np.dot(rel_vel, distance)) * rel_vel / (abs_distance ** 5))
        acceleration = np.sum(accelerations, axis=1)
        derivate_acceleration = np.sum(derivates_accelerations, axis=1)
        positions_pred = positions + stepsize * velocities + 0.5 * acceleration * stepsize ** 2 + (1/6) * derivate_acceleration * stepsize ** 3
        velocities_pred = velocities + stepsize * acceleration + 0.5 * derivate_acceleration * stepsize ** 2

        for body1 in range(bodycount):
            for body2 in range(bodycount):
                if body1 != body2:
                    distance = positions_pred[body2] - positions_pred[body1]
                    rel_vel = velocities_pred[body2] - velocities_pred[body1]
                    abs_distance = math.sqrt(distance[0] ** 2 + distance[1] ** 2 + distance[2] ** 2)
                    accelerations_pred[body1][body2] = gms[body2] * distance / (abs_distance ** 3)
                    derivates_accelerations_pred[body1][body2] = gms[body2] * (
                        (rel_vel/(abs_distance ** 3))
                        - 3 * (np.dot(rel_vel, distance)) * rel_vel / (abs_distance ** 5))

        acceleration_pred = np.sum(accelerations_pred, axis=1)
        derivate_acceleration_pred = np.sum(derivates_accelerations_pred, axis=1)

        acc_dev_2 = -6 * (acceleration - acceleration_pred)/(stepsize ** 2) - 2 * (2 * derivate_acceleration + derivate_acceleration_pred)/stepsize
        acc_dev_3 = 12 * (acceleration - acceleration_pred)/(stepsize ** 3) + 6 * (derivate_acceleration + derivate_acceleration_pred)/(stepsize ** 2)

        velocities = velocities_pred + 1/6 * acc_dev_2 * (stepsize ** 3) + 1/24 * acc_dev_3 * (stepsize ** 4)
        positions = positions_pred + 1/24 * acc_dev_2 * (stepsize ** 4) + 1/120 * acc_dev_3 * (stepsize ** 5)

        time -= stepsize
        count += 1
        if time <= 0:
            break

    return positions, velocities


class Hermite(Solver):

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
    test_solver = Hermite()
    # set scenario for solver
    test_solver.set_scenario(scen)
    time_difference = (date2 - date1)
    # run solver
    positions, velocities = test_solver.solve(int(time_difference.total_seconds()), 25)
    print((time_difference.total_seconds()) / (24 * 60 * 60) + ' Days')

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
    com = com_eval.evaluate(scen,positions,velocities, int(time_difference.total_seconds()))
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