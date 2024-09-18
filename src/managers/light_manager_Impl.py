try:
    from machine import PWM, Pin
except:
    ...
from src.managers.light_manager import LightManager_I
from logger_client import LoggerClient

class LightManager(LightManager_I):
    def __init__(self, pin, logger: LoggerClient, initial_brightness: int = 0):
        assert pin >= 0
        self.max_brightness = 75000
        self.med_brightness = 10000
        self.min_brightness = 0

        initial_brightness = min(self.max_brightness, initial_brightness)
        initial_brightness = max(self.min_brightness, initial_brightness)

        self.light = Pin(pin, Pin.OUT)
        self.brightness = initial_brightness
        if self.brightness > 0:
            self.on()

        self.pwm = PWM(pin)
        self.pwm.freq(100)
        self.pwm.duty_u16(self.brightness)

    def on(self):
        self.light.on()

    def off(self):
        self.light.off()

    def __set_brightness(self, brightness: int):
        self.pwm.duty_u16(brightness)
        if brightness == 0:
            self.off()
        else:
            self.on()
    
    def set_percent(self, percent: float):
        """Brightness from 0 to 1"""
        assert 0 <= percent <= 1
        brightness = int((self.max_brightness - self.min_brightness) * percent)
        self.__set_brightness(brightness)
