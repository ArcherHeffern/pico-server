from typing import Literal

class Config:
    DEBUG = True
    USING_PICO = True
    IP = "127.0.0.1"

class LocalConfig(Config):
    ...


class ConfigFactory:
    @staticmethod
    def get_config(environment: Literal["pico", "local"]) -> Config:
        match environment:
            case "pico":
                return Config()
            case "local":
                return LocalConfig()
        return Config
