from lib.http.server import RequestBuilder, Request, Response
from unittest import TestCase

http_request_str1 = """POST /echo HTTP/1.1
Host: reqbin.com
Pragma: no-cache
Content-Type: application/x-www-form-urlencoded
Content-Length: 35

key1=value1&key2=value2&key3=value3"""

http_request_str2 = """POST /echo?hello=world&teddy=bear HTTP/1.1
Host: reqbin.com
Pragma: no-cache
Content-Type: application/x-www-form-urlencoded
Content-Length: 35

key1=value1&key2=value2&key3=value3"""

class RequestTest(TestCase):
    def test_from_string(self):
        actual = RequestBuilder().from_string(http_request_str1)
        headers = {
            "Host": "reqbin.com",
            "Pragma": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "35"
        }
        expected = Request("/echo", "POST", "HTTP/1.1", headers, {}, "key1=value1&key2=value2&key3=value3")
        self.assertEqual(actual, expected)

    def test_from_string_with_query_params(self):
        actual = RequestBuilder().from_string(http_request_str2)
        headers = {
            "Host": "reqbin.com",
            "Pragma": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "35"
        }
        expected = Request("/echo", "POST", "HTTP/1.1", headers, {"hello": "world", "teddy": "bear"}, "key1=value1&key2=value2&key3=value3")
        self.assertEqual(actual, expected)
    
    def test_from_string_with_body(self):
        ...
    
    def test_from_string_with_form_body(self):
        ...
    
