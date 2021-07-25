import math

import solver
import tb_scenario
import hermite_solver

#Two Body Solver
class TB_Solver(solver.Solver):
    def __init__(self):
        self.scenario = None

    def set_scenario(self, scenario):
        self.scenario = scenario

    def solve(self, time, stepsize=None):
        if self.scenario is None:
            return 1
        masses = self.scenario.get_masses()
        positions = self.scenario.get_positions()
        velocities = self.scenario.get_velocities()
        gms = self.scenario.get_gms()

        print(masses)
        print(velocities)
        print(positions)
        print('')
        g = 6.67408E-11

        com_p = (positions[0] * gms[0] + positions[1] * gms[1])/(gms[0] + gms[1])
        com_v = (velocities[0] * gms[0] + velocities[1] * gms[1])/(gms[0] + gms[1])


        r0 = positions[0] #- com_p
        r1 = positions[1] #- com_p

        print(com_p)

        r0_abs = math.sqrt(r0[0] ** 2 + r0[1] ** 2 + r0[2] ** 2)
        r1_abs = math.sqrt(r1[0] ** 2 + r1[1] ** 2 + r1[2] ** 2)

        print(r0/r0_abs)
        print(r1/r1_abs)

        v0 = velocities[0] #- com_v
        v1 = velocities[1] #- com_v

        print(com_v)

        print(v0, v1)

        v0_2 = v0[0] ** 2 + v0[1] ** 2 + v0[2] ** 2
        v1_2 = v1[0] ** 2 + v1[1] ** 2 + v1[2] ** 2

        print(v0_2, v1_2)

        rm = masses[0] * masses[1] / (masses[0] + masses[1])
        rmg = gms[0] * gms[1] / (gms[0] + gms[1])

        sum_masses = masses[0] + masses[1]
        sum_0_cm = masses[0] + rm
        sum_1_cm = masses[1] + rm
        prod_0_cm = masses[0] * rm
        prod_1_cm = masses[1] * rm

        e0 = v0_2/2 - g * rm/r0_abs
        e1 = v1_2/2 - g * rm/r1_abs



        #a0 = -g * rm/2*e0
        #a1 = -g * rm/2*e1

        #a0 = -r0_abs * g * sum_0_cm / (v0_2 * r0_abs - g * sum_0_cm * 2)
        #a1 = -r1_abs * g * sum_1_cm / (v1_2 * r1_abs - g * sum_1_cm * 2)

        #a0 = -r0_abs * (g * rm **3 / sum_0_cm ** 2) / (v0_2 * r0_abs - (g * rm **3 / sum_0_cm ** 2) * 2)
        #a1 = -r1_abs * (g * rm **3 / sum_1_cm ** 2) / (v1_2 * r1_abs - (g * rm **3 / sum_1_cm ** 2) * 2)

        #a0 = - g * prod_0_cm/ (2 * (v0_2 * rm / 2 - g * prod_0_cm / r0_abs))
        #a1 = - g * prod_1_cm/ (2 * (v1_2 * rm / 2 - g * prod_1_cm / r1_abs))

        a0 = - rmg / (v0_2 / 2 - rmg / r0_abs)
        a1 = - rmg / (v1_2 / 2 - rmg / r1_abs)
        print(g * rm)
        print(v0_2 * rm / 2, g * prod_0_cm / r0_abs)
        print(v1_2 * rm / 2, g * prod_1_cm / r1_abs)
        #print(v0_2 / 2, g * rm / r0_abs)
        #print(v1_2 / 2, g * rm / r1_abs)
        com_p_t = com_p + com_v * time

        
        return e0, e1, a0, a1

def main():



    scen = tb_scenario.TBScenario((-1.553231269366519e+06, -1.365761028169902e+06, 5.178486173213917e+05),
                                  (-2.373121746016003, 1.087760755711206e+1, 2.156883918142271e+1),
                                  1.303e+22,
                                  (1.272597199894877e+07,1.118988405350912e+07,-4.243029459125704e+06),
                                  (1.944357613173209e+1,-8.912801268085466e+1,-1.767269776821415e+2),
                                  1.586e+21,
                                  8.696138177608748E+02, 1.058799888601881E+02)
    test_solver = TB_Solver()
    test_solver.set_scenario(scen)
    e0, e1, a0, a1 = test_solver.solve(365*24*60*60, 60)

    print(e0, e1, a0, a1)

    T = 2 * math.pi * math.sqrt(a0 ** 3 / 8.696138177608748E+02)
    print(T/(24*60*60))

    hermite_Solver = hermite_solver.Hermite()
    hermite_Solver.set_scenario(scen)
    positions, velocities = hermite_Solver.solve(T, 3600)
    print(positions)



if __name__ == "__main__":
    # execute only if run as a script
    main()
