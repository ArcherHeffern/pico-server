from lib.http.types import TextBody
from lib.http.request import Request
from lib.http.response import Response
from lib.http.router import Router

web_router = Router()

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

@web_router.get("/")
def get_root(request: Request) -> Response:
    return Response(200, TextBody(html))