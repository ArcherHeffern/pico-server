from lib.http.server import Server
from pathlib import Path
from lib.http.router import Router
from lib.http.request_builder import RequestBuilder
from lib.http.types import TextBody
from lib.http.request import Request
from lib.http.response import Response
from services import logger

class HTTPServer:
    def __init__(self):
        self.routes = {}
        self.static_paths: set = set()
    
    def run(self, ip: str = "127.0.0.1", port: int = 8080, callback = None):
        Server().listen(logger, self.handler, ip, port, callback)
    
    def handler(self, request_str: str) -> str:
        maybe_request = RequestBuilder().from_string(request_str)
        if maybe_request:
            logger.log(f"Client requested {maybe_request.method} {maybe_request.url}")
        response = self.__request_handler(maybe_request)
        return response.to_string()


    def __add_route(self, route: str, method: str, handler):
        self.routes[(route, method)] = handler
    
    def get(self, route: str):
        def _handler(func):
            self.__add_route(route, "GET", func)
        return _handler

    def post(self, route: str):
        def _handler(func):
            self.__add_route(route, "POST", func)
        return _handler
    
    def use_router(self, router: Router):
        self.routes.update(router.routes)

    def add_static_path(self, path: str):
        """Raises exception if path does not exist"""
        path_p: Path = Path(path)
        if not path_p.exists():
            raise FileNotFoundError(path)
        self.static_paths.add(path_p)

    def __request_handler(self, request: Request|None) -> Response:
        if not request:
            return Response(400)
        handler = self.routes.get((request.url, request.method))
        if handler:
            return handler(request)
        # Check for static file
        maybe_response = self.__check_in_static_path(request)
        if maybe_response:
            return maybe_response
        return Response(404)
    
    def __check_in_static_path(self, request: Request) -> Response|None:
        target_path = Path(request.url.removeprefix("/"))
        for s in self.static_paths:
            if not self.__is_subpath(target_path, s):
                continue
            try:
                with open(target_path, "r") as f:
                    file_contents = f.read()
                    return Response(200, TextBody(file_contents))
            except Exception as e:
                if isinstance(e, FileNotFoundError):
                    continue
                return Response(500, TextBody(f"Failed to open file {request.url}"))
        return None
    
    def __is_subpath(self, main: Path, subpath: Path):
        if len(subpath.parts) > len(main.parts):
            return False
        for bse, lng in zip(subpath.parts, main.parts):
            if bse != lng:
                return False
        return True