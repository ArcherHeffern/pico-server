from src.managers.light_manager_Impl import LightManager
from logger_client import LoggerClient

class LightManager_D(LightManager):
    def __init__(self, pin, logger: LoggerClient, initial_brightness: int = 0):
        self.percent = initial_brightness
        self.pin = pin
        self.logger = logger
        self._on = True

    def on(self):
        self.logger.log(f"[Light {self.pin}] turned on")
        self._on = True

    def off(self):
        self.logger.log(f"[Light {self.pin}] turned off")
        self._on = False

    def set_percent(self, percent: float):
        self.logger.log(f"[Light {self.pin}] set to {percent*100} percent")
        """Sets brightness to a percent. Turns light on or off if necessary"""
        self.percent = percent
        if percent == 0:
            self._on = False
        else:
            self._on = True