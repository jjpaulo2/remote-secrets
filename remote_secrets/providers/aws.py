import json

from remote_secrets.providers._base import SecretManager

try:
    from boto3 import client

except ImportError:
    raise EnvironmentError('You must install "remote-secrets[aws]" extras!')


class AWSParameterStoreManager(SecretManager):
    def __init__(self, region: str | None = None):
        self.client = client("ssm", region_name=region)

    def secret(self, name: str) -> dict:
        return self.client.get_parameter(Name=name, WithDecryption=True)

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

    def delete(self, name: str, **kwargs):
        self.client.delete_parameter(Name=name)

    def list(self) -> list[str]:
        return [
            secret["Name"] for secret in self.client.describe_parameters()["Parameters"]
        ]


class AWSSecretManager(SecretManager):
    def __init__(self, region: str | None = None):
        self.client = client("secretsmanager", region_name=region)

    def secret(self, name: str) -> dict:
        return self.client.get_secret_value(SecretId=name)

    def get(self, name: str) -> str:
        return self.secret(name)["SecretString"]

    def get_json(self, name: str) -> dict[str, str]:
        return json.loads(self.secret(name)["SecretString"])

    def update(self, name: str, value: str):
        self.client.update_secret(SecretId=name, SecretString=value)

    def update_json(self, name: str, value: dict[str, str]):
        self.update(name, json.dumps(value))

    def delete(self, name: str, **kwargs):
        self.client.delete_secret(SecretId=name, **kwargs)

    def list(self) -> list[str]:
        return [secret["Name"] for secret in self.client.list_secrets()["SecretList"]]
