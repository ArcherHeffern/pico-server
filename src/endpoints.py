
from lib.http.types import TextBody
from lib.http.server import Request, Response
from services import light_manager, logger

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

def get_root(request: Request) -> Response:
    return Response(200, TextBody(html))

def get_brightness(request: Request) -> Response:
    return Response(200, TextBody(str(light_manager.percent)))

def set_brightness(request: Request) -> Response:
    param = request.query_params.get("b")
    if not param:
        return Response(400)
    try:
        new_brightness = int(param)
    except:
        return Response(400)
    new_brightness = new_brightness / 100
    light_manager.set_percent(new_brightness)
    return Response(200, TextBody(str(new_brightness)))