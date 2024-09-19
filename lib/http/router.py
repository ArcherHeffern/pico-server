class Router:
    def __init__(self):
        self.routes: dict = {}

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