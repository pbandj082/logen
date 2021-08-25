from abc import ABCMeta, abstractmethod
from typing import Callable

from .logger import Logger
from .formatter import Formatter, LogRecord
from .handlers import FileHandler
from .handlers import ConsoleHandler


class Factory(metaclass=ABCMeta):
    @abstractmethod
    def get_logger(self, module_name: str) -> Logger:
        ...
    
    @abstractmethod
    def create_formatter(
        self,
        fmt_func: Callable[[LogRecord], str],
    ) -> Formatter:
        ...

    @abstractmethod
    def create_file_handler(
        self,
        file_name: str,
        max_bytes: int = 2000,
        backup_count: int = 5,
        encoding: str = 'UTF-8',
    ) -> FileHandler:
        ...
    
    @abstractmethod
    def create_console_handler(self) -> ConsoleHandler:
        ...
