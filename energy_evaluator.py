from evaluator import Evaluator
import com_evaluator
import numpy as np
import math

# should use mass but gm means it is just multiplied by g
def get_kinetic_energy(velocities, gms):
    T = 0
    for v_i in range(velocities.shape[0]):
        T += 0.5 * gms[v_i] * (velocities[v_i][0] ** 2 + velocities[v_i][1] ** 2 + velocities[v_i][2] ** 2)
    return T

# should use mass but gm means it is just multiplied by g
def get_potential_energy(positions, gms):
    V = 0
    for p_i in range(positions.shape[0]):
        for p_j in range(positions.shape[0]):
            if p_i != p_j:
                distance = positions[p_i] - positions[p_j]
                V -= 0.5 * gms[p_i] * gms[p_j] / (math.sqrt(distance[0] ** 2 + distance[1] ** 2 + distance[2] ** 2))
    return V


class Energy_Evaluator(Evaluator):

    # should use mass but gm means it is just multiplied by g
    def evaluate(self, scenario, positions, velocities, time=None):
        com_v_0 = com_evaluator.get_com_vel(scenario.get_velocities(), scenario.get_gms())
        T_0 = get_kinetic_energy(scenario.get_velocities() + com_v_0, scenario.get_gms())
        V_0 = get_potential_energy(scenario.get_positions(), scenario.get_gms())
        E_0 = T_0 + V_0

        com_v_t = com_evaluator.get_com_vel(velocities, scenario.get_gms())
        T_t = get_kinetic_energy(velocities + com_v_t, scenario.get_gms())
        V_t = get_potential_energy(positions, scenario.get_gms())
        E_t = T_t + V_t

        return T_0, V_0, T_t, V_t, E_0, E_t
