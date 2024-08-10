import json

try:
    from google.cloud.secretmanager import SecretManagerServiceClient, AccessSecretVersionResponse

except ImportError:
    raise EnvironmentError('You must install \"remote-secrets[gcp]\" extras!')


class GCPSecretManager:

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = SecretManagerServiceClient()

    def secret_name(self, name: str) -> str:
        return f'projects/{self.project_id}/secrets/{name}/versions/latest'

    def secret(self, name: str) -> AccessSecretVersionResponse:
        return self.client.access_secret_version(name=self.secret_name(name))

    def get(self, name: str) -> str:
        return self.secret(name).payload.data.decode()
    
    def get_json(self, name: str) -> dict[str, str]:
        return json.loads(self.secret(name).payload.data)
    