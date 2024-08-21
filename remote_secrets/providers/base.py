from abc import ABC
from typing import Any


class MethodNotSupported(NotImplementedError):

    def __init__(self, method_name: str, class_name: str) -> None:
        self.method_name = method_name
        self.class_name = class_name
        super().__init__(f'Method "{method_name}" not supported for class "{class_name}"!')


class SecretManager(ABC):
    client: Any

    def secret(self, name: str) -> Any:
        raise MethodNotSupported('secret', type(self).__name__)
    
    def get(self, name: str) -> str:
        raise MethodNotSupported('get', type(self).__name__)
    
    def get_list(self, name: str) -> list[str]:
        raise MethodNotSupported('get_list', type(self).__name__)
    
    def get_json(self, name: str) -> dict[str, str]:
        raise MethodNotSupported('get_json', type(self).__name__)
    
    def list(self) -> list[str]:
        raise MethodNotSupported('list', type(self).__name__)
    
    def set(self, name: str, value: str):
        raise MethodNotSupported('set', type(self).__name__)
    
    def load(self):
        raise MethodNotSupported('load', type(self).__name__)
    