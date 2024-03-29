from abc import ABCMeta, abstractmethod
from enum import Enum
import time
from typing import Optional, NamedTuple


class ConsoleColor:
    def __init__(self, fg_sequence: str, bg_sequence: str):
        self._fg_sequence = fg_sequence
        self._bg_sequence = bg_sequence
    
    @property
    def fg_sequence(self) -> str:
        return self._fg_sequence

    @property
    def bg_sequence(self) -> str:
        return self._bg_sequence


class ConsoleColors:
    black = ConsoleColor('\033[30m', '\033[40m')
    bright_black = ConsoleColor('\033[90m', '\033[100m')
    red = ConsoleColor('\033[31m', '\033[41m')
    bright_red = ConsoleColor('\033[91m', '\033[101m')
    green = ConsoleColor('\033[32m', '\033[42m')
    bright_green = ConsoleColor('\033[92m', '\033[102m')
    yellow = ConsoleColor('\033[33m', '\033[43m')
    bright_yellow = ConsoleColor('\033[93m', '\033[103m')
    blue = ConsoleColor('\033[34m', '\033[44m')
    bright_blue = ConsoleColor('\033[94m', '\033[104m')
    magenta = ConsoleColor('\033[35m', '\033[45m')
    bright_magenta = ConsoleColor('\033[95m', '\033[105m')
    cyan = ConsoleColor('\033[36m', '\033[46m')
    bright_cyan = ConsoleColor('\033[96m', '\033[106m')
    white = ConsoleColor('\033[37m', '\033[47m')
    bright_white = ConsoleColor('\033[97m', '\033[107m')


class StyledConsole(metaclass=ABCMeta):
    @abstractmethod
    def sequence_string(self) -> str: ...


class ConsoleMessage(StyledConsole):
    def __init__(self, message: str):
        self._message = message
    
    def sequence_string(self) -> str:
        return f'{self._message}\033[0m'


class ForeColoring(StyledConsole):
    def __init__(self, child: StyledConsole, color: ConsoleColor):
        self._child = child
        self._color = color

    def sequence_string(self) -> str:
        return f'{self._color.fg_sequence}{self._child.sequence_string()}'


class BackColoring(StyledConsole):
    def __init__(self, child: StyledConsole, color: ConsoleColor):
        self._child = child
        self._color = color

    def sequence_string(self) -> str:
        return f'{self._color.bg_sequence}{self._child.sequence_string()}'


class Formatter(metaclass=ABCMeta):
    ...


class LogRecord(NamedTuple):
    message: Optional[str] = None
    module_name: Optional[str] = None
    level: Optional[str] = None
    line_no: Optional[int] = None
    timestamp: Optional[float] = None
    milliseconds: Optional[int] = None
    stack_trace: Optional[str] = None
    console_msg: Optional[str] = None
    process: Optional[str] = None


level_color_map = {
    'DEBUG': ConsoleColors.bright_magenta,
    'INFO': ConsoleColors.bright_green,
    'WARNING': ConsoleColors.bright_yellow,
    'ERROR': ConsoleColors.bright_red,
    'CRITICAL': ConsoleColors.bright_red,
}


def console_log_format_function(record: LogRecord):
    time_format = f'%Y-%m-%d %H:%M:%S.{record.milliseconds:03d}%z'
    created_at = ForeColoring(
        child=ConsoleMessage(
            time.strftime(
                time_format,
                time.localtime(record.timestamp),
            ),
        ),
        color=ConsoleColors.bright_blue,
    ).sequence_string()
    process = ''
    if record.process is not None:
        process_id = ForeColoring(
            child=ConsoleMessage(record.process),
            color=ConsoleColors.bright_cyan
        ).sequence_string()
        process = f' [{process_id}]'
    level_color = level_color_map[record.level]
    level = ForeColoring(
        child=ConsoleMessage(record.level),
        color=level_color,
    ).sequence_string()
    message = record.console_msg or record.message
    called_from = ''
    if record.level == 'DEBUG':
        called_from = f' ({record.module_name}:{record.line_no or ""})'
    stack_trace = ''
    if record.stack_trace:
        stack_trace = ForeColoring(
            child=ConsoleMessage(f'\n{record.stack_trace}'),
            color=level_color_map['ERROR'],
        ).sequence_string()
    s = f'{created_at}{process} {level + ":":16s} {message}{called_from}{stack_trace}'
    return s


def standard_log_format_function(record: LogRecord):
    time_format = f'%Y-%m-%d %H:%M:%S.{record.milliseconds:03d}%z'
    created_at = time.strftime(
        time_format,
        time.localtime(record.timestamp),
    )
    process = ''
    if record.process is not None:
        process = f' [{record.process}]'
    level = record.level
    message = record.message
    called_from = ''
    if record.level == 'DEBUG':
        called_from = f' ({record.module_name}:{record.line_no or ""})'
    stack_trace = ''
    if record.stack_trace:
        stack_trace = f'\n{record.stack_trace}'
    s = f'{created_at}{process} {level + ":":8s} {message}{called_from}{stack_trace}'
    return s

