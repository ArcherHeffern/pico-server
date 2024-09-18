from dataclasses import dataclass, field
from typing import ClassVar, Type
from lib.http.types import ResponseBody, NoBody

@dataclass
class Response:
    status_code: int
    body: ResponseBody = NoBody()
    headers: dict[str, str] = field(default_factory=dict) # type: ignore
    http_version: str = "HTTP/1.1"
    STATUS_CODE_TO_REASON: ClassVar[dict[int, str]] = {
        100: "Continue",
        101: "Switching Protocols",
        200: "OK",
        201: "Created",
        202: "Accepted",
        203: "Non-Authoritative Information",
        204: "No Content",
        205: "Reset Content",
        206: "Partial Content",
        300: "Multiple Choices",
        301: "Moved Permanently",
        302: "Found",
        303: "See Other",
        304: "Not Modified",
        305: "Use Proxy",
        307: "Temporary Redirect",
        400: "Bad Request",
        401: "Unauthorized",
        402: "Payment Required",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        406: "Not Acceptable",
        407: "Proxy Authentication Required",
        408: "Request Time-out",
        409: "Conflict",
        410: "Gone",
        411: "Length Required",
        412: "Precondition Failed",
        413: "Request Entity Too Large",
        414: "Request-URI Too Large",
        415: "Unsupported Media Type",
        416: "Requested range not satisfiable",
        417: "Expectation Failed",
        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Time-out",
        505: "HTTP Version not supported",
    }
    # TODO: Support different response types

    def to_string(self) -> str:
        request_line = self.http_version + " " + str(self.status_code) + " " + Response.STATUS_CODE_TO_REASON[self.status_code]
        headers = []
        body = self.__body_to_string()
        headers = self.__headers_to_string(len(body))
        return request_line + "\n" + headers + "\n" + body

    def __headers_to_string(self, body_length: int) -> str:
        headers = []

        if body_length > 0:
            self.headers["Content-Length"] = str(body_length)
        if not self.headers:
            return ""
        for k, v in self.headers.items():
            headers.append(f"{k}: {v}")
        header_string = "\n".join(headers) + "\n"
        return header_string
    
    def __body_to_string(self) -> str:
        return self.body.to_string()