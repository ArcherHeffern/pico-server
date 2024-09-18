from abc import ABC, abstractmethod
from logger_client import LoggerClient

class LightManager_I(ABC):
    def __init__(self, pin, logger: LoggerClient, initial_brightness: int = 0):
        raise NotImplemented()

    @abstractmethod
    def on(self):
        raise NotImplemented()

    @abstractmethod
    def off(self):
        raise NotImplemented()

    @abstractmethod
    def set_percent(self, percent: float):
        """Sets brightness to a percent. Turns light on or off if necessary"""
        raise NotImplemented()