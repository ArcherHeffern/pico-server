from lib.http.request import Request
from lib.http.response import Response
from lib.http.router import Router
from services import lcd_manager
from lib.util import parse_str_to_bool

lcd_router = Router()

@lcd_router.post("/lcd")
def print_lcd(request: Request) -> Response:
    msg = request.body
    append = request.query_params.get("append")
    to_append = False
    if not append:
        to_append = False
    else:
        maybe_to_append = parse_str_to_bool(append)
        if maybe_to_append is None:
            return Response(400)
        to_append = maybe_to_append
    if not to_append:
        lcd_manager.clear()
    lcd_manager.print(msg)
    return Response(200)