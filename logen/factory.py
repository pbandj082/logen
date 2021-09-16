from abc import ABCMeta, abstractmethod
from typing import Callable

from .logger import Logger
from .formatter import Formatter, LogRecord, standard_log_format_function
from .handlers import FileHandler, ConsoleHandler
from .manager import Manager


class Factory(metaclass=ABCMeta):
    @abstractmethod
    def acquire_logger(self, module_name: str) -> Logger:
        ...
    
    @abstractmethod
    def create_formatter(
        self,
        fmt_func: Callable[[LogRecord], str] = standard_log_format_function,
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
    
    @property
    @abstractmethod
    def manager() -> Manager: ...
    