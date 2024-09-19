from socket import socket, SOL_SOCKET, SO_REUSEADDR
from io import BytesIO
from src.modules.logger import LoggerClient

BUFFER_SIZE = 1024

class Server:

    def __echo(self, s: str) -> str:
        return s

    def listen(self, logger: LoggerClient, handler = __echo, ip: str = "127.0.0.1", port: int = 8080, callback = None):
        address = (ip, port)
        connection = socket()
        connection.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        connection.bind(address)
        connection.listen(1)
        if callback:
            callback()
        while 1:
            client_socket: socket= connection.accept()[0]
            maybe_request_str = self.__read_request(client_socket)
            if not maybe_request_str:
                client_socket.close()
                continue
            response_str: str = handler(maybe_request_str)
            if not self.__send_response(response_str, client_socket):
                logger.error(f"Sending response")
            client_socket.close()

    def __read_request(self, client: socket) -> str|None:
        request_buffer = BytesIO()
        while tmp := client.recv(BUFFER_SIZE): 
            request_buffer.write(tmp)
            if len(tmp) != BUFFER_SIZE:
                break
        request_bytes = request_buffer.getvalue()
        request_str = bytes.decode(request_bytes, encoding="utf-8")
        return request_str

    def __send_response(self, response: str, client_socket: socket) -> bool:
        b = str.encode(response)
        client_socket.sendall(b)
        return True
