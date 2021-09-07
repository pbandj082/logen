from abc import ABCMeta
import logging
import logging.handlers

from .formatter import LoggingFormatter
from .level import to_logging_level
from ...handlers import Handler, ConsoleHandler, FileHandler
from ...level import Level


@Handler.register
class LoggingHandler(metaclass=ABCMeta):
    def __init__(self, origin: logging.Handler):
        self._origin = origin
    
    @property
    def origin(self) -> logging.Handler:
        return self._origin

    def set_formatter(self, formatter: LoggingFormatter) -> None:
        self._origin.setFormatter(formatter.origin)

    def set_level(self, level: Level) -> None:
        self._origin.setLevel(to_logging_level(level))


@ConsoleHandler.register
class LoggingConsoleHandler(LoggingHandler):
    def __init__(self, origin: logging.StreamHandler):
        super().__init__(origin=origin)


@FileHandler.register
class LoggingFileHandler(LoggingHandler):
    def __init__(self, origin: logging.handlers.RotatingFileHandler):
        super().__init__(origin=origin)


def create_logging_console_handler() -> LoggingConsoleHandler:
    origin = logging.StreamHandler()
    handler = LoggingConsoleHandler(origin=origin)
    return handler


def create_logging_file_handler(
    file_name: str,
    max_bytes: int = 2000_000,
    backup_count: int = 5,
    encoding: str = 'UTF-8',
) -> LoggingFileHandler:
    origin = logging.handlers.RotatingFileHandler(
        file_name,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding=encoding,
    )
    file_handler = LoggingFileHandler(origin=origin)
    return file_handler