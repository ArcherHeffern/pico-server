from lib.http.HTTPServer import HTTPServer
from src.resources.web import web_router
from src.resources.lamp import lamp_router
from src.resources.lcd import lcd_router

app = HTTPServer()

app.use_router(web_router)
app.use_router(lamp_router)
app.use_router(lcd_router)

app.add_static_path("static")

if __name__ == '__main__':
    ip = "127.0.0.1"
    port = 8080
    app.run(ip, port, lambda: print(f"Listening at {ip}:{port}"))
