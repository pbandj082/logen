import logging
from typing import Callable


from .formatter import create_logging_formatter
from .handlers import create_logging_console_handler, create_logging_file_handler
from .logger import get_logging_logger
from ...factory import Factory
from ...formatter import Formatter, LogRecord
from ...factory import Factory
from ...logger import Logger
from ...handlers import ConsoleHandler
from ...handlers import FileHandler


@Factory.register
class LoggingFactory:
    def get_logger(self, module_name: str) -> Logger:
        logger = get_logging_logger(module_name)
        return logger

    def create_formatter(
        self,
        format_function: Callable[[LogRecord], str],
    ) -> Formatter:
        formatter = create_logging_formatter(format_function)
        return formatter

    def create_console_handler(self) -> ConsoleHandler:
        console_handler = create_logging_console_handler()
        return console_handler


    def create_file_handler(
        self,
        file_name: str,
        max_bytes: int = 2000_000,
        backup_count: int = 5,
        encoding: str = 'UTF-8',
    ) -> FileHandler:
        file_handler = create_logging_file_handler(
            file_name=file_name,
            max_bytes=max_bytes,
            backup_count=backup_count,
            encoding=encoding,
        )
        return file_handler
