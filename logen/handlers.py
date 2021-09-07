from abc import ABCMeta, abstractmethod
from typing import Any

from .formatter import Formatter
from .level import Level


class Handler(metaclass=ABCMeta):
    @abstractmethod
    def set_formatter(self, formatter: Formatter) -> None:
        ...
    
    @abstractmethod
    def set_level(self, level: Level):
        ...


class FileHandler(Handler, metaclass=ABCMeta):
    ...


class ConsoleHandler(Handler, metaclass=ABCMeta):
    ...
