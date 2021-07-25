from evaluator import Evaluator
import com_evaluator
import numpy as np

# should use mass but gm means it is just multiplied by g
def get_angular_momentum(positions, velocities, gms):
    return np.sum(gms[:, None] * np.cross(positions, velocities), axis=-2) / np.sum(gms)

# Angular momentum evaluator
class AM_Evaluator(Evaluator):

    #
    def evaluate(self, scenario, positions, velocities, time=None):
        com_p_0 = com_evaluator.get_com_pos(scenario.get_positions(), scenario.get_gms())
        com_v_0 = com_evaluator.get_com_vel(scenario.get_velocities(), scenario.get_gms())
        am_0 = get_angular_momentum(scenario.get_positions() + com_p_0, scenario.get_velocities() + com_v_0, scenario.get_gms())

        com_p_t = com_evaluator.get_com_pos(positions, scenario.get_gms())
        com_v_t = com_evaluator.get_com_vel(velocities, scenario.get_gms())
        am_t = get_angular_momentum(positions + com_p_t, velocities + com_v_t, scenario.get_gms())

        return am_0, am_t
