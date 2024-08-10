import json

try:
    from boto3 import client

except ImportError:
    raise EnvironmentError('You must install \"remote-secrets[aws]\" extras!')


class AWSParameterStoreManager:

    def __init__(self, region: str | None = None):
        self.client = client('ssm', region_name=region)

    def secret(self, name: str) -> dict:
        return self.client.get_parameter(Name=name, WithDecryption=True)

    def get(self, name: str) -> str:
        return self.secret(name)['Parameter']['Value']
    
    def get_list(self, name: str) -> list[str]:
        secret = self.secret(name)
        if secret['Parameter']['Type'] != 'StringList':
            raise ValueError(f'The secret {name} is not a StringList!', name)
        return [
            secret
            for secret in self.secret(name)['Parameter']['Value'].split(',')
        ]


class AWSSecretManager:

    def __init__(self, region: str | None = None):
        self.client = client('secretsmanager', region_name=region)

    def secret(self, name: str) -> dict:
        return self.client.get_secret_value(SecretId=name)

    def get(self, name: str) -> str:
        return self.secret(name)['SecretString']

    def get_json(self, name: str) -> dict[str, str]:
        return json.loads(self.secret(name)['SecretString'])
    