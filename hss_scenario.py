import numpy

import scenario
import masses
import gm
import datetime
from astroquery.jplhorizons import Horizons
import numpy as np
import collections

#HORIZONS Solar System Scenario
class HSSScenario(scenario.Scenario):
    def __init__(self, date_time):
        self.ssb = '500@0' # Solar system barycenter in HORIZONS
        self.masses = masses.masses
        self.gm = gm.gm
        for object_id in self.gm:
            self.gm[object_id] *= 1000000000
        Y = date_time.year
        M = date_time.month
        D = date_time.day
        self.JDN = int(1461 * (Y + 4800 + int((M - 14)/12))/4) + int((367 * (M - 2 - 12 * int((M - 14)/12)))/12) - int((3 * int((Y + 4900 + int((M - 14)/12))/100))/4) + D - 32075
        self.JDN += -0.5 + (date_time.hour * 3600 + date_time.minute * 60 + date_time.second)/(24 * 3600)

        self.velocities = {}
        self.positions = {}
        for object_id in self.masses.keys():
            obj = Horizons(id_type='id', id=object_id, location=self.ssb, epochs=self.JDN)
            vec = obj.vectors()
            vec['x'].convert_unit_to('meter')
            vec['y'].convert_unit_to('meter')
            vec['z'].convert_unit_to('meter')
            vec['vx'].convert_unit_to('meter/s')
            vec['vy'].convert_unit_to('meter/s')
            vec['vz'].convert_unit_to('meter/s')
            self.velocities[object_id] = np.asarray((vec['vx'][0], vec['vy'][0], vec['vz'][0]))
            self.positions[object_id] = np.asarray((vec['x'][0], vec['y'][0], vec['z'][0]))

    def get_velocities(self):
        return numpy.array(list(collections.OrderedDict(sorted(self.velocities.items())).values()), dtype=float)

    def get_positions(self):
        return numpy.array(list(collections.OrderedDict(sorted(self.positions.items())).values()), dtype=float)

    def get_masses(self):
        return numpy.fromiter(collections.OrderedDict(sorted(self.masses.items())).values(), dtype=float)

    def get_ids(self):
        return list(collections.OrderedDict(sorted(self.masses.items())).keys())

    def get_julian_date(self):
        return self.JDN

    def get_gms(self):
        return numpy.fromiter(collections.OrderedDict(sorted(self.gm.items())).values(), dtype=float)

def main():
    scen = HSSScenario(datetime.datetime(2021, 6, 23, 14, 48, 53))
    print(scen.get_julian_date()) # should be 2459389.11728

    earth_id = '399'
    obj = Horizons(id_type='id', id=earth_id, location='500@0', epochs=scen.get_julian_date())
    vec = obj.vectors()
    vec['x'].convert_unit_to('meter')
    print(vec['x'][0])

    moon_id = '301'
    obj = Horizons(id_type='id', id=moon_id, location='500@0', epochs=scen.get_julian_date())
    vec = obj.vectors()
    vec['x'].convert_unit_to('kilometer')
    print(vec['x'][0])

    vec['vx'].convert_unit_to('meter/s')
    print(vec['vx'][0])
    vec['vy'].convert_unit_to('meter/s')
    print(vec['vy'][0])
    vec['vz'].convert_unit_to('meter/s')
    print(vec['vz'][0])

    print(len(masses.masses))

    print(scen.get_masses().dtype)
    print(scen.get_masses())

    print(scen.get_positions().dtype)
    print(scen.get_positions())

    print(scen.get_velocities().dtype)
    print(scen.get_velocities())

if __name__ == "__main__":
    # execute only if run as a script
    main()