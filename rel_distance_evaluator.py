from evaluator import Evaluator
import numpy as np
import math

# Relative distance divided by velocity
class Rel_Distance_Evaluator(Evaluator):

    def evaluate(self, scenario, positions, velocities, time = None):
        positions2 = scenario.get_positions()
        velocities2 = scenario.get_velocities()
        ids = scenario.get_ids()
        distance_time = {}
        for body in range(len(scenario.get_masses())):
            distance = positions[body] - positions2[body]
            distance_abs = math.sqrt(distance[0] ** 2 + distance[1] ** 2 + distance[2] ** 2)
            velocity_abs = math.sqrt(
                velocities2[body][0] ** 2 + velocities2[body][1] ** 2 + velocities2[body][2] ** 2)
            distance_time[ids[body]] = distance_abs / velocity_abs

        return distance_time