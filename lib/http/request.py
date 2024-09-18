from typing import ClassVar, Literal

class Request:
    Method = ClassVar[Literal["OPTIONS", "GET", "HEAD", "POST", "PUT", "DELETE", "TRACE", "CONNECT"]]

    def __init__(self, url: str, method: Method, version, headers, query_params, body: str|dict):
        self.url: str = url
        self.method: Request.Method = method
        self.version: str = version
        self.headers: dict[str, str] = headers
        self.query_params: dict[str, str] = query_params
        self.body: str