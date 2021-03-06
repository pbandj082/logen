from abc import ABCMeta, abstractmethod
from typing import Optional

from .handlers import Handler
from .level import Level


class Logger(metaclass=ABCMeta):
    @abstractmethod
    def debug(self, msg: str, console_msg: Optional[str] = None) -> None:
        ...

    @abstractmethod
    def info(self, msg: str, console_msg: Optional[str] = None) -> None:
        ...

    @abstractmethod
    def warning(self, msg: str, console_msg: Optional[str] = None) -> None:
        ...
    
    @abstractmethod
    def error(self, msg: str, console_msg: Optional[str] = None, show_trace: bool = False) -> None:
        ...
   
    @abstractmethod
    def critical(self, msg: str, console_msg: Optional[str] = None, show_trace: bool = False) -> None:
        ...

    @abstractmethod
    def add_handler(self, handler: Handler) -> None:
        ...

    @abstractmethod
    def set_level(self, level: Level) -> None:
        ...

