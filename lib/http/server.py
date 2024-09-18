from socket import socket, SOL_SOCKET, SO_REUSEADDR
from lib.http.request_builder import RequestBuilder
from lib.http.request import Request
from lib.http.response import Response
from io import BytesIO
from typing import TypeAlias, Callable, Optional 
import services

BUFFER_SIZE = 1024

class Server:

    Handler: TypeAlias = Callable[[Request], Response]

    def __init__(self):
        self.routes: dict[tuple[str, Request.Method], Server.Handler] = {}

    def add_route(self, route: str, method: Request.Method, handler: Callable[[Request], Response]):
        self.routes[(route, method)] = handler

    def add_routes(self, routes: dict[tuple[str, Request.Method], Handler]):
        for endpoint, handler in routes.items():
            route, method = endpoint
            self.add_route(route, method, handler)

    def listen(self, ip = "127.0.0.1", port = 8080, callback: Optional[Callable[[], None]] = None):
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

        
    def __read_request(self, client: socket) -> Optional[str]:
        services.logger.log("BEGIN reading request")
        request_buffer = BytesIO()
        while tmp := client.recv(BUFFER_SIZE): # Stuck here...
            request_buffer.write(tmp)
            if len(tmp) != BUFFER_SIZE:
                break
        request_bytes = request_buffer.getvalue()
        request_str = bytes.decode(request_bytes, encoding="utf-8")
        services.logger.log("END reading request")
        return request_str

    def __request_handler(self, request: Optional[Request]) -> Response:
        if not request:
            return Response(400)
        handler = self.routes.get((request.url, request.method))
        if not handler:
            return Response(404)
        return handler(request)
    
    def __send_response(self, response: Response, client_socket: socket) -> bool:
        s = response.to_string()
        b = str.encode(s)
        client_socket.sendall(b)
        return True

