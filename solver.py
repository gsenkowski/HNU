import abc

class Solver(abc.ABC):
    @abc.abstractmethod
    def set_scenario(self, scenario):
        pass

    @abc.abstractmethod
    def solve(self, time, stepsize):
        pass

