from pathlib import Path
from abc import ABC, abstractmethod


class AbstractDigitalTWINBase(ABC):
    operator = None

    def __init__(self, operator):
        self.operator = operator



