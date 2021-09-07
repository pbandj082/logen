import logging

from ...formatter import Formatter, LogRecord
from typing import Callable


@Formatter.register
class LoggingFormatter:
    def __init__(self, origin: logging.Formatter):
        self._origin = origin

    @property
    def origin(self) -> logging.Formatter:
        return self._origin


class _LoggingFormatter(logging.Formatter):
    def __init__(self, format_function: Callable[[LogRecord], str]):
        super().__init__()
        self._fmt_func = format_function

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


def create_logging_formatter(
    format_function: Callable[[LogRecord], str],
) -> LoggingFormatter:
    origin = _LoggingFormatter(format_function=format_function)
    return LoggingFormatter(origin=origin)
