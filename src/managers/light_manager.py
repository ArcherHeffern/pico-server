from logger_client import LoggerClient

class LightManager_I:
    def __init__(self, pin, logger: LoggerClient, initial_brightness: int = 0):
        raise NotImplemented()

    def on(self):
        raise NotImplemented()

    def off(self):
        raise NotImplemented()

    def set_percent(self, percent: float):
        """Sets brightness to a percent. Turns light on or off if necessary"""
        raise NotImplemented()