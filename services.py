from config import ConfigFactory
from src.managers.light_manager_Impl import LightManager
from src.managers.light_manager_Dbg import LightManager_D
from logger_client import LoggerClient

config = ConfigFactory.get_config("local")

logger = LoggerClient(config.DEBUG)

if config.USING_PICO:
    light_manager = LightManager(16, logger)
else:
    light_manager = LightManager_D(16, logger)