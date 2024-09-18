from typing import Type
import json
from abc import ABC, abstractmethod

def select_body_from_content_type_header(content_type: str) -> Type['ResponseBody']:
    content_type = content_type.split(";", 1)[0].strip()
    if "application/json":
        return JsonBody
    if "multipart/form-data":
        raise NotImplementedError()
    if "application/x-www-form-urlencoded":
        raise NotImplementedError()
    if "form-data":
        return FormBody
    return TextBody


class ResponseBody(ABC):
    name: str

    @abstractmethod
    def to_string(self) -> str:
        raise NotImplementedError()
    
    @abstractmethod
    def from_string(self) -> str:
        raise NotImplementedError()
    
class NoBody(ResponseBody):
    def to_string(self):
        return ""

    def from_string(self):
        ...

class JsonBody(ResponseBody):
    def __init__(self, json: dict):
        self.json = json

    def to_string(self):
        json.dumps(self.json)
    
    def from_string(self):
        ...

class FormBody(ResponseBody):
    def __init__(self, form: dict[str, str]):
        self.form = form

    def to_string(self):
        ...
    
    def from_string(self):
        ...


class TextBody(ResponseBody):
    def __init__(self, text: str):
        self.text = text
    
    def to_string(self):
        return self.text
    
    def from_string(self):
        ...
