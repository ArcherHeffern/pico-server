from unittest import TestCase
from lib.http.types import TextBody
from lib.http.response import Response

http_response_str = """HTTP/1.1 200 OK
Date: Thu, Jul  3 15:27:54 2014
Content-Type: text/xml; charset="utf-8"
Connection: close

"""

class ResponseTest(TestCase):
    def test_to_string(self):
        actual = Response(200).to_string()
        expected = "HTTP/1.1 200 OK\n\n"
        self.assertEqual(actual, expected)
        
    
    def test_to_string_query_params(self):
        ...

    def test_to_string_plain_body(self):
        actual = Response(200, TextBody("Hello world")).to_string()
        expected = "HTTP/1.1 200 OK\nContent-Length: 11\n\nHello world"
        self.assertEqual(actual, expected)
    
    def test_to_string_form(self):
        ...