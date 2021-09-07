import logging

from ...level import Level
from typing import Dict


def to_logging_level(level: Level):
    return logging_levels_map[level]


logging_levels_map: Dict[Level, int] = {
    Level.debug: logging.DEBUG,
    Level.info: logging.INFO,
    Level.warning: logging.WARNING,
    Level.error: logging.ERROR,
    Level.critical: logging.CRITICAL,
}