class Config:
    DEBUG = True
    USING_PICO = False
    IP = "127.0.0.1"

class LocalConfig(Config):
    ...


class ConfigFactory:
    @staticmethod
    def get_config(environment: str) -> Config:
        if "pico":
            return Config()
        if "local":
            return LocalConfig()
        return Config()
