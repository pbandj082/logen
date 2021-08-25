from abc import ABCMeta, abstractmethod

from .handlers import Handler
from .level import Level


class Logger(metaclass=ABCMeta):
    @abstractmethod
    def debug(self, msg: str) -> None:
        ...

    @abstractmethod
    def info(self, msg: str) -> None:
        ...

    @abstractmethod
    def warning(self, msg: str) -> None:
        ...
    
    @abstractmethod
    def error(self, msg: str, show_trace: bool) -> None:
        ...
   
    @abstractmethod
    def critical(self, msg: str) -> None:
        ...

    @abstractmethod
    def add_handler(self, handler: Handler) -> None:
        ...

    @abstractmethod
    def set_level(self, level: Level) -> None:
        ...

