import abc

class Scenario(abc.ABC):

    @abc.abstractmethod
    def get_masses(self):
        pass

    @abc.abstractmethod
    def get_velocities(self):
        pass

    @abc.abstractmethod
    def get_positions(self):
        pass

    @abc.abstractmethod
    def get_gms(self):
        pass

    @abc.abstractmethod
    def get_ids(self):
        pass
