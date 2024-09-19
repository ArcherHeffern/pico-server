from socket import socket, SOL_SOCKET, SO_REUSEADDR
from lib.http.request_builder import RequestBuilder
from lib.http.types import TextBody
from lib.http.request import Request
from lib.http.response import Response
from io import BytesIO
from pathlib import Path
import services

BUFFER_SIZE = 1024

class Server:

    def __init__(self):
        self.routes = {}
        self.static_paths: set = set()

    def add_route(self, route: str, method: str, handler):
        self.routes[(route, method)] = handler

    def add_routes(self, routes):
        for endpoint, handler in routes.items():
            route, method = endpoint
            self.add_route(route, method, handler)
        
    def add_static_path(self, path: str):
        """Raises exception if path does not exist"""
        path_p: Path = Path(path)
        if not path_p.exists():
            raise FileNotFoundError(path)
        self.static_paths.add(path_p)

    def listen(self, ip = "127.0.0.1", port = 8080, callback = None):
        address = (ip, port)
        connection = socket()
        connection.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        connection.bind(address)
        connection.listen(1)
        if callback:
            callback()
        while 1:
            client_socket, client_ip = connection.accept()
            client_socket: socket
            client_ip: str
            maybe_request_str = self.__read_request(client_socket)
            if not maybe_request_str:
                client_socket.close()
                continue
            maybe_request = RequestBuilder().from_string(maybe_request_str)
            if maybe_request:
                services.logger.log(f"Client {client_ip} requested {maybe_request.method} {maybe_request.url}")
            response = self.__request_handler(maybe_request)
            if not self.__send_response(response, client_socket):
                services.logger.error(f"Sending response to {client_ip}")
            client_socket.close()

        
    def __read_request(self, client: socket) -> str|None:
        request_buffer = BytesIO()
        while tmp := client.recv(BUFFER_SIZE): # Stuck here...
            request_buffer.write(tmp)
            if len(tmp) != BUFFER_SIZE:
                break
        request_bytes = request_buffer.getvalue()
        request_str = bytes.decode(request_bytes, encoding="utf-8")
        return request_str

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
    
    def __send_response(self, response: Response, client_socket: socket) -> bool:
        s = response.to_string()
        b = str.encode(s)
        client_socket.sendall(b)
        return True

