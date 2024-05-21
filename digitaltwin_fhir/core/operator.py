from abc import ABC, abstractmethod
from .base import Loader, Create


class AbstractOperator(ABC):
    core = None

    def __init__(self, core):
        self.core = core

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class Operator(AbstractOperator):
    load_class = Loader
    create_class = Create

    def __init__(self, core):
        super().__init__(core)

    def load(self):
        return self.load_class(self, self.core)

    def create(self):
        return self.create_class(self, self.core)

    def update(self):
        pass

    def delete(self):
        pass
