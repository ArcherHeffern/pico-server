
class Request:
    Methods = ("GET", "POST", "HEAD", "PATCH", "PUT", "DELETE", "OPTIONS")
    def __init__(self, url: str, method: str, version: str, headers, query_params: dict[str, str], body: str|dict):
        self.url: str = url
        self.method: str = method
        self.version: str = version
        self.headers: dict[str, str] = headers
        self.query_params: dict[str, str] = query_params
        self.body: str|dict = body