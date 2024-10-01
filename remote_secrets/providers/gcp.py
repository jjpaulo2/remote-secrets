import json

from remote_secrets.providers._base import SecretManager

try:
    from google.cloud.secretmanager import (
        SecretManagerServiceClient,
        AccessSecretVersionResponse,
    )
    from google.cloud.resourcemanager_v3 import ProjectsClient
    from google.auth import default

except ImportError:
    raise EnvironmentError('You must install "remote-secrets[gcp]" extras!')


class GCPSecretManager(SecretManager):
    def __init__(self, project_id: str | None = None):
        self._project: str | None = None
        self.client = SecretManagerServiceClient()
        self.project_id = project_id
        if self.project_id is None:
            _, self.project_id = default()

    @property
    def project(self) -> str:
        if self._project is None:
            credentials, _ = default()
            client = ProjectsClient(credentials=credentials)
            project = client.get_project(name=f"projects/{self.project_id}")
            self._project = project.name
        return self._project

    def secret_name(self, name: str) -> str:
        return f"{self.project}/secrets/{name}/versions/latest"

    def secret(self, name: str) -> AccessSecretVersionResponse:
        return self.client.access_secret_version(name=self.secret_name(name))

    def get(self, name: str) -> str:
        return self.secret(name).payload.data.decode()

    def get_json(self, name: str) -> dict[str, str]:
        return json.loads(self.secret(name).payload.data)

    def list(self) -> list[str]:
        request = {"parent": self.project}
        return [secret.name for secret in self.client.list_secrets(request)]
