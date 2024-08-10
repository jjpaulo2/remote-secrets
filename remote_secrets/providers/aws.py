from typing import Type
from boto3 import client

from remote_secrets.types import CastType


class AWSParameterStoreManager:

    def __init__(self, region: str | None = None):
        self.client = client('ssm', region_name=region)

    def secret(self, name: str) -> dict:
        return self.client.get_parameter(Name=name, WithDecryption=True)

    def get(self, name: str, cast: Type[CastType]) -> CastType:
        return cast(self.secret(name)['Parameter']['Value']) # type: ignore
    
    def get_list(self, name: str, cast: Type[CastType]) -> list[CastType]:
        secret = self.secret(name)
        if secret['Parameter']['Type'] != 'StringList':
            raise ValueError(f'The secret {name} is not a StringList!', name)
        return [
            cast(secret.strip()) # type: ignore
            for secret in self.secret(name)['Parameter']['Value'].split(',')
            if isinstance(secret, str)
        ]


class AWSSecretManager:

    def __init__(self, region: str | None = None):
        self.client = client('secretsmanager', region_name=region)

    def secret(self, name: str) -> dict:
        return self.client.get_secret_value(SecretId=name)

    def get(self, name: str, cast: Type[CastType]) -> CastType:
        return cast(self.secret(name)['SecretString']) # type: ignore
