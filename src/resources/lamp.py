from lib.http.request import Request
from lib.http.response import Response
from lib.http.types import TextBody
from lib.http.router import Router

lamp_router = Router()

# Client
from services import light_manager

@lamp_router.get("/brightness")
def brightness(request: Request) -> Response:
    return Response(200, TextBody(str(light_manager.percent)))

@lamp_router.post("/brightness")
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