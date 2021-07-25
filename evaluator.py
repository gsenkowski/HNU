import abc

class Evaluator(abc.ABC):

    @abc.abstractmethod
    def evaluate(self, scenario, positions, velocities, time):
        pass