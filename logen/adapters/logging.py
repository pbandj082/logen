from abc import ABCMeta
import logging
import logging.handlers
import io
import sys
import traceback
from typing import Optional, Tuple, Callable, Dict

from ..formatter import Formatter, LogRecord
from ..factory import Factory
from ..logger import Logger
from ..handlers import Handler
from ..handlers import ConsoleHandler
from ..handlers import FileHandler
from ..level import Level

logging_levels_map: Dict[Level, int] = {
    Level.debug: logging.DEBUG,
    Level.info: logging.INFO,
    Level.warning: logging.WARNING,
    Level.error: logging.ERROR,
    Level.critical: logging.CRITICAL,
}


def to_logging_level(level: Level):
    return logging_levels_map[level]


class LoggingFormatter(Formatter):
    def __init__(self, origin: logging.Formatter):
        self._origin = origin

    @property
    def origin(self) -> logging.Formatter:
        return self._origin


class _LoggingFormatter(logging.Formatter):
    def __init__(self, fmt_func: Callable[[LogRecord], str]):
        super().__init__()
        self._fmt_func = fmt_func
    
    def format(self, record: logging.LogRecord) -> str:
        message = record.getMessage()
        module_name = record.name
        level = record.levelname
        line_no = record.lineno
        timestamp = record.created
        milliseconds = record.msecs
        stack_trace = None
        if record.exc_info:
            if record.exc_text:
                stack_trace = record.exc_text
            else:
                stack_trace = self.formatException(record.exc_info)
        s = self._fmt_func(
            LogRecord(
                message=message,
                module_name=module_name,
                level=level,
                line_no=line_no,
                timestamp=timestamp,
                milliseconds=milliseconds,
                stack_trace=stack_trace
            )
        )
        return s


class LoggingHandler(Handler, metaclass=ABCMeta):
    def __init__(self, origin: logging.Handler):
        self._origin = origin
    
    @property
    def origin(self) -> logging.Handler:
        return self._origin

    def set_formatter(self, formatter: Formatter) -> None:
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


class LoggingLogger(Logger):
    def __init__(self, origin: logging.Logger):
        self._origin = origin 

    def debug(self, msg: str) -> None:
        self._origin.debug(msg)

    def info(self, msg: str) -> None:
        self._origin.info(msg)

    def warning(self, msg: str) -> None:
        self._origin.warning(msg)

    def error(self, msg: str, show_trace=False) -> None:
        self._origin.error(msg, exc_info=show_trace)
    
    def critical(self, msg: str, show_trace=False) -> None:
        self._origin.critical(msg, exc_info=show_trace)
    
    def add_handler(self, handler: Handler) -> None:
        self._origin.addHandler(handler.origin)
    
    def set_level(self, level: Level) -> None:
        self._origin.setLevel(to_logging_level(level))


class _LoggingLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name=name, level=level)
    
    def findCaller(self, stack_info: bool, stacklevel: int) -> Tuple[str, int, str, Optional[str]]:
        f = sys._getframe(3)
        if f is not None:
            f = f.f_back
        orig_f = f
        while f and stacklevel > 1:
            f = f.f_back
            stacklevel -= 1
        if not f:
            f = orig_f
        rv = '(unknown file)', 0, '(unknown function)', None
        if hasattr(f, 'f_code'):
            co = f.f_code
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
        return rv


class LoggingFactory(Factory):
    def get_logger(self, module_name: str) -> Logger:
        logging.setLoggerClass(_LoggingLogger)
        origin = logging.getLogger(module_name)
        logger = LoggingLogger(origin=origin)
        return logger

    def create_formatter(
        self,
        fmt_func: Callable[[LogRecord], str]
    ) -> Formatter:
        origin = _LoggingFormatter(fmt_func=fmt_func)
        formatter = LoggingFormatter(origin=origin)
        return formatter

    def create_console_handler(self) -> ConsoleHandler:
        origin = logging.StreamHandler()
        console_handler = LoggingConsoleHandler(origin=origin)
        return console_handler

    def create_file_handler(
        self,
        file_name: str,
        max_bytes: int = 2000_000,
        backup_count: int = 5,
        encoding: str = 'UTF-8',
    ) -> FileHandler:
        origin = logging.handlers.RotatingFileHandler(
            file_name,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding=encoding,
        )
        file_handler = LoggingFileHandler(origin=origin)
        return file_handler
