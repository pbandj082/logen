import logging

from ...manager import Manager


@Manager.register
class LoggingManager:
    def __init__(self, origin: logging.Manager):
        self._origin = origin
    
    @property
    def origin(self):
        return self._origin
    
    @property
    def logger_map(self):
        return self._origin.loggerDict


manager = LoggingManager(origin=logging.Logger.manager)
