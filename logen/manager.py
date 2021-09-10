from abc import ABCMeta, abstractmethod


from typing import Dict

from .logger import Logger


class Manager(metaclass=ABCMeta):
    @property
    @abstractmethod
    def logger_map() -> Dict[str, Logger]: ...
