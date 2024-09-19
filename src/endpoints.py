
from lib.http.types import TextBody
from lib.http.server import Request, Response
from services import light_manager, logger, lcd_manager

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

def print_lcd(request: Request) -> Response:
    msg = request.body
    append = request.query_params.get("append")
    to_append = False
    if not append:
        to_append = False
    else:
        maybe_to_append = __parse_str_to_bool(append)
        if maybe_to_append is None:
            return Response(400)
        to_append = maybe_to_append
    if not to_append:
        lcd_manager.clear()
    lcd_manager.print(msg)
    return Response(200)

def __parse_str_to_bool(b: str) -> bool|None:
    b = b.lower()
    if b == "true":
        return True
    elif b == "false":
        return False
    return None

