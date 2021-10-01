from typing import Callable


from .formatter import create_logging_formatter
from .handlers import create_logging_console_handler, create_logging_file_handler
from .logger import acquire_logging_logger
from .manager import manager as logging_manager
from ...factory import Factory
from ...formatter import Formatter, LogRecord, standard_log_format_function, console_log_format_function
from ...factory import Factory
from ...logger import Logger
from ...handlers import ConsoleHandler
from ...handlers import FileHandler
from ...manager import Manager


@Factory.register
class LoggingFactory:
    def acquire_logger(self, module_name: str) -> Logger:
        logger = acquire_logging_logger(module_name)
        return logger

    def create_formatter(
        self,
        format_function: Callable[[LogRecord], str] = standard_log_format_function,
    ) -> Formatter:
        formatter = create_logging_formatter(format_function)
        return formatter

    def create_console_handler(self) -> ConsoleHandler:
        console_handler = create_logging_console_handler()
        console_handler.set_formatter(self.create_formatter(console_log_format_function))
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
        file_handler.set_formatter(self.create_formatter())
        return file_handler
    

    @property
    def manager(self) -> Manager:
        return logging_manager
