import json
from typing import Mapping

from remote_secrets.exceptions import SecretNotFoundException
from remote_secrets.providers._base import SecretManager

try:
    from boto3 import client
    from types_boto3_secretsmanager import SecretsManagerClient
    from types_boto3_ssm import SSMClient
    from botocore.exceptions import ClientError

except ImportError:
    raise EnvironmentError('You must install "remote-secrets[aws]" extras!')


class AWSParameterStoreManager(SecretManager):
    client: SSMClient

    def __init__(self, region: str | None = None):
        self.client = client("ssm", region_name=region)

    def secret(self, name: str) -> Mapping:
        try:
            return self.client.get_parameter(Name=name, WithDecryption=True)
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ResourceNotFoundException":
                raise SecretNotFoundException(name)
            raise exc

    def get(self, name: str) -> str:
        return self.secret(name)["Parameter"]["Value"]

    def get_list(self, name: str) -> list[str]:
        secret = self.secret(name)
        if secret["Parameter"]["Type"] != "StringList":
            raise ValueError(f"The secret {name} is not a StringList!", name)
        return [
            secret.strip()
            for secret in self.secret(name)["Parameter"]["Value"].split(",")
        ]

    def update(self, name: str, value: str):
        self.client.put_parameter(Name=name, Value=value, Overwrite=True)

    def update_list(self, name: str, value: list[str]):
        self.update(name, ", ".join(value))

    def create(self, name: str, value: str, **kwargs):
        args = {"Name": name, "Value": value, "Type": "SecureString"}
        args.update(kwargs)
        self.client.put_parameter(**args)

    def create_list(self, name: str, value: list[str], **kwargs):
        kwargs.update({"Type": "StringList"})
        self.create(name, ", ".join(value), **kwargs)

    def delete(self, name: str, **kwargs):
        self.client.delete_parameter(Name=name)

    def list(self) -> list[str]:
        return [
            secret["Name"] for secret in self.client.describe_parameters()["Parameters"]
        ]


class AWSSecretManager(SecretManager):
    client: SecretsManagerClient

    def __init__(self, region: str | None = None):
        self.client = client("secretsmanager", region_name=region)

    def secret(self, name: str) -> Mapping:
        try:
            return self.client.get_secret_value(SecretId=name)
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ResourceNotFoundException":
                raise SecretNotFoundException(name)
            raise exc

    def get(self, name: str) -> str:
        return self.secret(name)["SecretString"]

    def get_json(self, name: str) -> dict[str, str]:
        return json.loads(self.secret(name)["SecretString"])

    def update(self, name: str, value: str):
        self.client.update_secret(SecretId=name, SecretString=value)

    def update_json(self, name: str, value: dict[str, str]):
        self.update(name, json.dumps(value))

    def create(self, name: str, value: str, **kwargs):
        self.client.create_secret(Name=name, SecretString=value, **kwargs)

    def create_json(self, name: str, value: dict[str, str], **kwargs):
        self.create(name, json.dumps(value), **kwargs)

    def delete(self, name: str, **kwargs):
        self.client.delete_secret(SecretId=name, **kwargs)

    def list(self) -> list[str]:
        return [secret["Name"] for secret in self.client.list_secrets()["SecretList"]]
