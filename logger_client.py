class LoggerClient:
    def __init__(self, enabled):
        self.enabled = enabled

    def log(self, msg: str):
        if self.enabled:
            print(msg)

    def info(self, msg: str):
        if self.enabled:
            self.log("[INFO] " + msg)

    def warning(self, msg: str):
        if self.enabled:
            self.log("[WARNING] " + msg)
    
    def error(self, msg: str):
        if self.enabled:
            self.log("[ERROR] " + msg)

    def critical(self, msg: str):
        if self.enabled:
            self.log("[CRITICAL] " + msg)