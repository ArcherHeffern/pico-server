from src.managers.logger_client import LoggerClient
try:
    from lib.display.lcd1602 import LCD1602
    from machine import Pin, I2C
except:
    ...

class LcdManager:
    def __init__(self):
        i2c = I2C(1,scl=Pin(7), sda=Pin(6), freq=400000)
        d = LCD1602(i2c, 2, 16) 
        self.__lcd_manager = d
    
    def print(self, s: str):
        self.__lcd_manager.print(s)
    
    def clear(self):
        self.__lcd_manager.clear()