from abc import ABC, abstractmethod


class Benchmark(ABC):
    def __init__(self, logger):
        self.logger = logger

    @abstractmethod
    def run(self):
        """Execute the benchmark logic."""
        pass
