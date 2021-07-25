from evaluator import Evaluator
import numpy as np

def get_com_pos(positions, gms):
    return np.sum(gms[:, None] * positions, axis=-2) / np.sum(gms)

def get_com_vel(velocities, gms):
    return np.sum(gms[:, None] * velocities, axis=-2) / np.sum(gms)
# Center of mass evaluator
class COM_Evaluator(Evaluator):

    #
    def evaluate(self, scenario, positions, velocities, time):
        com_vel_0 = get_com_vel(scenario.get_velocities(), scenario.get_gms())
        com_vel_t = get_com_vel(velocities, scenario.get_gms())
        com_pos_0 = get_com_pos(scenario.get_positions(), scenario.get_gms())
        com_pos_t = get_com_pos(positions, scenario.get_gms())
        com_pos_0_t = com_pos_0 + com_vel_0 * time

        return com_vel_0, com_vel_t, com_pos_0, com_pos_t, com_pos_0_t