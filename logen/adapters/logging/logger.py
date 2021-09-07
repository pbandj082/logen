import io
import sys
import traceback
import logging
from typing import Optional, Tuple

from ...logger import Logger
from .handlers import LoggingHandler
from .level import Level, to_logging_level


@Logger.register
class LoggingLogger:
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
    
    def add_handler(self, handler: LoggingHandler) -> None:
        self._origin.addHandler(handler.origin)
    
    def set_level(self, level: Level) -> None:
        self._origin.setLevel(to_logging_level(level))
    

class _LoggingLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name=name, level=level)
    
    def findCaller(
        self,
        stack_info: bool = False,
        stacklevel: int = 1
    ) -> Tuple[str, int, str, Optional[str]]:
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


def get_logging_logger(module_name: str) -> LoggingLogger:
    logging.setLoggerClass(_LoggingLogger)
    origin = logging.getLogger(module_name)
    return LoggingLogger(origin=origin)
