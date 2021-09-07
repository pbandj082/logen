from abc import ABCMeta, abstractmethod
from pydantic import BaseModel, Field
import time
from typing import Optional


class ConsoleColor(metaclass=ABCMeta):
    @abstractmethod
    def fg_sequence(self) -> str: ...

    @abstractmethod
    def bg_sequence(self) -> str: ...


class ConsoleBlack(ConsoleColor):
    def __init__(self, bright=False):
        self._bright = bright

    def fg_sequence(self) -> str:
        sequence = '\033[90m' if self._bright else '\033[30m'
        return sequence

    def bg_sequence(self) -> str:
        sequence = '\033[100m' if self._bright else '\033[40m'
        return sequence


class ConsoleRed(ConsoleColor):
    def __init__(self, bright=False):
        self._bright = bright

    def fg_sequence(self) -> str:
        sequence = '\033[91m' if self._bright else '\033[31m'
        return sequence

    def bg_sequence(self) -> str:
        sequence = '\033[101m' if self._bright else '\033[41m'
        return sequence


class ConsoleGreen(ConsoleColor):
    def __init__(self, bright=False):
        self._bright = bright

    def fg_sequence(self) -> str:
        sequence = '\033[92m' if self._bright else '\033[32m'
        return sequence

    def bg_sequence(self) -> str:
        sequence = '\033[102m' if self._bright else '\033[42m'
        return sequence


class ConsoleYellow(ConsoleColor):
    def __init__(self, bright=False):
        self._bright = bright

    def fg_sequence(self) -> str:
        sequence = '\033[93m' if self._bright else '\033[33m'
        return sequence

    def bg_sequence(self) -> str:
        sequence = '\033[103m' if self._bright else '\033[43m'
        return sequence


class ConsoleBlue(ConsoleColor):
    def __init__(self, bright=False):
        self._bright = bright

    def fg_sequence(self) -> str:
        sequence = '\033[94m' if self._bright else '\033[34m'
        return sequence

    def bg_sequence(self) -> str:
        sequence = '\033[104m' if self._bright else '\033[44m'
        return sequence


class ConsoleMagenta(ConsoleColor):
    def __init__(self, bright=False):
        self._bright = bright

    def fg_sequence(self) -> str:
        sequence = '\033[95m' if self._bright else '\033[35m'
        return sequence

    def bg_sequence(self) -> str:
        sequence = '\033[105m' if self._bright else '\033[45m'
        return sequence


class ConsoleCyan(ConsoleColor):
    def __init__(self, bright=False):
        self._bright = bright

    def fg_sequence(self) -> str:
        sequence = '\033[96m' if self._bright else '\033[36m'
        return sequence

    def bg_sequence(self) -> str:
        sequence = '\033[106m' if self._bright else '\033[46m'
        return sequence


class ConsoleWhite(ConsoleColor):
    def __init__(self, bright=False):
        self._bright = bright

    def fg_sequence(self) -> str:
        sequence = '\033[97m' if self._bright else '\033[37m'
        return sequence

    def bg_sequence(self) -> str:
        sequence = '\033[107m' if self._bright else '\033[47m'
        return sequence


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
        return f'{self._color.fg_sequence()}{self._child.sequence_string()}'


class BackColoring(StyledConsole):
    def __init__(self, child: StyledConsole, color: ConsoleColor):
        self._child = child
        self._color = color

    def sequence_string(self) -> str:
        return f'{self._color.bg_sequence()}{self._child.sequence_string()}'


class Formatter(metaclass=ABCMeta):
    ...


class LogRecord(BaseModel):
    module_name: Optional[str] = Field(None)
    message: Optional[str] = Field(None)
    level: Optional[str] = Field(None)
    line_no: Optional[int] = Field(None)
    timestamp: Optional[float] = Field(None)
    milliseconds: Optional[int] = Field(None)
    stack_trace: Optional[str] = Field(None)


level_color_map = {
    'DEBUG': ConsoleWhite(bright=True),
    'INFO': ConsoleGreen(bright=True),
    'WARNING': ConsoleYellow(bright=True),
    'ERROR': ConsoleRed(bright=True),
    'CRITICAL': ConsoleRed(bright=True),
}


def standard_console_log_format_function(record: LogRecord):
    time_format = f'%Y-%m-%d %H:%M:%S.{record.milliseconds:03d}%z'
    created_at = ForeColoring(
        child=ConsoleMessage(
            time.strftime(
                time_format,
                time.localtime(record.timestamp),
            ),
        ),
        color=ConsoleBlue(bright=True),
    ).sequence_string()
    level_color = level_color_map[record.level]
    level = BackColoring(
        child=ForeColoring(
            child=ConsoleMessage(record.level),
            color=ConsoleBlack(),
        ),
        color=level_color,
    ).sequence_string()
    message = record.message
    called_from = ''
    if record.level == 'DEBUG':
        called_from = f'({record.module_name}:{record.line_no or ""})'
    stack_trace = ''
    if record.stack_trace:
        stack_trace = ForeColoring(
            child=ConsoleMessage(f'\n{record.stack_trace}'),
            color=level_color_map['ERROR'],
        ).sequence_string()
    s = f'{created_at} {level + ":":24s} {message} {called_from} {stack_trace}'
    return s


def standard_file_log_format_function(record: LogRecord):
    time_format = f'%Y-%m-%d %H:%M:%S.{record.milliseconds:03d}%z'
    created_at = time.strftime(
        time_format,
        time.localtime(record.timestamp),
    )
    level = record.level
    message = record.message
    called_from = ''
    if record.level == 'DEBUG':
        called_from = f'({record.module_name}:{record.line_no or ""})'
    stack_trace = ''
    if record.stack_trace:
        stack_trace = f'\n{record.stack_trace}'
    s = f'{created_at} {level + ":":8s} {message} {called_from} {stack_trace}'
    return s

