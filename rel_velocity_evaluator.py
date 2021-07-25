from evaluator import Evaluator
import numpy as np
import math

# Relative distance divided by velocity
class Rel_Velocity_Evaluator(Evaluator):

    def evaluate(self, scenario, positions, velocities, time = None):
        positions2 = scenario.get_positions()
        velocities2 = scenario.get_velocities()
        ids = scenario.get_ids()
        rel_velocities = {}
        for body in range(len(scenario.get_masses())):
            velocity_abs1 = math.sqrt(velocities[body][0] ** 2 + velocities[body][1] ** 2 + velocities[body][2] ** 2)
            velocity_abs2 = math.sqrt(velocities2[body][0] ** 2 + velocities2[body][1] ** 2 + velocities2[body][2] ** 2)
            velocity_abs_diff = velocity_abs1 - velocity_abs2
            rel_velocities[ids[body]] = velocity_abs_diff

        return rel_velocities