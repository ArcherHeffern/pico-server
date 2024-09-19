from io import StringIO
from src.modules.logger import LoggerClient

class LcdManager_D:
    def __init__(self, logger: LoggerClient):
        self.buffer = StringIO()
        self.logger = logger
    
    def print(self, s: str):
        self.buffer.write(s)
        self.logger.log(f"LCD: {self.buffer.getvalue()}")
    
    def clear(self):
        self.buffer = StringIO()
        self.logger.log(f"LCD: Cleared")