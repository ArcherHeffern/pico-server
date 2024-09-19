from config import ConfigFactory
from src.managers.light_manager_Impl import LightManager
from src.managers.light_manager_Dbg import LightManager_D
from src.managers.lcd_manager_Impl import LcdManager
from src.managers.lcd_manager_Dbg import LcdManager_D
from src.managers.logger_client import LoggerClient

config = ConfigFactory.get_config("local")

logger = LoggerClient(config.DEBUG)

if config.USING_PICO:
    light_manager = LightManager(16)
    lcd_manager = LcdManager()
else:
    light_manager = LightManager_D(16, logger)
    lcd_manager = LcdManager_D(logger)
