import json

from remote_secrets.providers.base import SecretManager

try:
    from google.cloud.secretmanager import SecretManagerServiceClient, AccessSecretVersionResponse

except ImportError:
    raise EnvironmentError('You must install \"remote-secrets[gcp]\" extras!')


class GCPSecretManager(SecretManager):

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = SecretManagerServiceClient()

    @property
    def parent(self) -> str:
        return f'projects/{self.project_id}'

    def secret_name(self, name: str) -> str:
        return f'{self.parent}/secrets/{name}/versions/latest'

    def secret(self, name: str) -> AccessSecretVersionResponse:
        return self.client.access_secret_version(name=self.secret_name(name))

    def get(self, name: str) -> str:
        return self.secret(name).payload.data.decode()
    
    def get_json(self, name: str) -> dict[str, str]:
        return json.loads(self.secret(name).payload.data)
    
    def list(self) -> list[str]:
        request = {"parent": self.parent}
        return [
            secret.name
            for secret in self.client.list_secrets(request)
        ]
