from enum import Enum
import logging
from typing import Dict


class Level(int, Enum):
    debug: int = 10
    info: int =  20
    warning: int = 30
    error: int = 40
    critical: int = 50
