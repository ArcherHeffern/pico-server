from lib.http.request import Request
from lib.http.parse_utils import ParseUtils
from typing import Optional
from services import logger

class RequestBuilder:
    def __init__(self):
        self.__url: str = "/"
        self.__method: Request.Method = "GET"
        self.__version: str = "HTTP/1.1"
        self.__headers: dict[str, str] = {} 
        self.__query_params: dict[str, str] = {}
        self.__body: str = ""

    def from_string(self, request: str) -> Optional['Request']:
        lines = request.splitlines()
        request_line = lines[0]
        if not self.__parse_request_line(request_line):
            logger.warning(f"Failed to parse request line: {request_line}")
            return None

        i = 1
        while lines[i].strip() != "":
            line = lines[i]
            k, v = map(str.strip, line.split(":", 1))
            self.__headers[k] = v
            i += 1
        self.__body = "\n".join(lines[i+1:])
        return Request(self.__url, self.__method, self.__version, self.__headers, self.__query_params, self.__body)
    
    def __parse_request_line(self, request_line: str) -> bool:
        """Method SP Request-URI SP HTTP-Version CRLF"""
        tokens = request_line.split(" ")
        if len(tokens) != 3:
            return False

        method = tokens[0]
        if not self.__parse_url(tokens[1]):
            return False
        self.__version = tokens[2]

        if method not in Request.Method.__args__[0].__args__:
            return False
        else:
            self.__method = method # type: ignore
        return True
    
    def __parse_url(self, url: str) -> bool:
        """
        @return bool: If successfully parses url and query string parameters
        """
        if not url:
            return False
        tokens = url.split("?", 1)
        url = tokens[0]
        self.__url = url
        if len(tokens) == 1:
            return True
        param_sect = tokens[1]
        params = ParseUtils.parse_key_values(param_sect, "&", "=")
        self.__query_params = params
        return True