from abc import ABC
from typing import Any

from remote_secrets.exceptions import MethodNotSupported


class SecretManager(ABC):
    client: Any

    def secret(self, name: str) -> Any:
        raise NotImplementedError

    def get(self, name: str) -> str:
        raise MethodNotSupported("get", type(self).__name__)

    def get_list(self, name: str) -> list[str]:
        raise MethodNotSupported("get_list", type(self).__name__)

    def get_json(self, name: str) -> dict[str, str]:
        raise MethodNotSupported("get_json", type(self).__name__)

    def load(self):
        raise MethodNotSupported("load", type(self).__name__)

    def update(self, name: str, value: str):
        raise MethodNotSupported("update", type(self).__name__)

    def update_list(self, name: str, value: list[str]):
        raise MethodNotSupported("update_list", type(self).__name__)

    def update_json(self, name: str, value: dict[str, str]):
        raise MethodNotSupported("update_json", type(self).__name__)

    def create(self, name: str, value: str, **kwargs):
        raise MethodNotSupported("create", type(self).__name__)

    def create_list(self, name: str, value: list[str], **kwargs):
        raise MethodNotSupported("create_list", type(self).__name__)

    def create_json(self, name: str, value: dict[str, str], **kwargs):
        raise MethodNotSupported("create_json", type(self).__name__)

    def delete(self, name: str, **kwargs):
        raise MethodNotSupported("delete", type(self).__name__)

    def list(self) -> list[str]:
        raise MethodNotSupported("list", type(self).__name__)
