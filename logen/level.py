from enum import IntEnum
import logging
from typing import Dict


class Level(IntEnum):
    debug: int = 10
    info: int =  20
    warning: int = 30
    error: int = 40
    critical: int = 50
