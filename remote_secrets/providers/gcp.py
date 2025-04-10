import json

from remote_secrets.exceptions import SecretNotFoundException
from remote_secrets.providers._base import SecretManager

try:
    from google.api_core.exceptions import NotFound
    from google.cloud.secretmanager import (
        SecretManagerServiceClient,
        AccessSecretVersionResponse,
    )
    from google.cloud.resourcemanager_v3 import ProjectsClient
    from google.auth import default
    from google_crc32c import Checksum

except ImportError:
    raise EnvironmentError('You must install "remote-secrets[gcp]" extras!')


class GCPSecretManager(SecretManager):
    client: SecretManagerServiceClient

    def __init__(self, project_id: str | None = None):
        self._project: str | None = None
        self.client = SecretManagerServiceClient()
        self.project_id = self._get_project_id(project_id)

    @property
    def project(self) -> str:
        if self._project is None:
            credentials, _ = default()
            client = ProjectsClient(credentials=credentials)
            project = client.get_project(name=f"projects/{self.project_id}")
            self._project = project.name
        return self._project

    def _get_project_id(self, project_id: str | None) -> str:
        if not project_id:
            _, project_id = default()
        return str(project_id)

    def _get_value_checksum(self, value: str) -> int:
        check = Checksum()
        check.update(value.encode())
        return int(check.hexdigest(), 16)

    def secret_versions(self, name: str) -> list[str]:
        try:
            versions = self.client.list_secret_versions(
                request={"parent": self.client.secret_path(self.project_id, name)}
            )
            return [ver.name for ver in versions]
        except NotFound:
            return []

    def secret(self, name: str) -> AccessSecretVersionResponse:
        try:
            return self.client.access_secret_version(name=self.secret_versions(name)[0])
        except IndexError:
            raise SecretNotFoundException(name)

    def get(self, name: str) -> str:
        return self.secret(name).payload.data.decode()

    def get_json(self, name: str) -> dict[str, str]:
        return json.loads(self.secret(name).payload.data)

    def update(self, name: str, value: str):
        self.client.add_secret_version(
            request={
                "parent": self.client.secret_path(self.project_id, name),
                "payload": {
                    "data": value.encode(),
                    "data_crc32c": self._get_value_checksum(value),
                },
            }
        )
        secret_versions = self.secret_versions(name)
        if len(secret_versions) > 1:
            self.client.disable_secret_version(request={"name": secret_versions[1]})

    def update_json(self, name: str, value: dict[str, str]):
        self.update(name, json.dumps(value))

    def create(self, name: str, value: str, **kwargs):
        self.client.create_secret(
            request={
                "parent": f"projects/{self.project_id}",
                "secret_id": name,
                "secret": {
                    "ttl": kwargs.get("ttl"),
                    "replication": {"automatic": {}},
                },
            }
        )
        self.update(name, value)

    def create_json(self, name: str, value: dict[str, str], **kwargs):
        self.create(name, json.dumps(value), **kwargs)

    def delete(self, name: str, **kwargs):
        self.client.delete_secret(
            request={"name": self.client.secret_path(self.project_id, name)}
        )

    def list(self) -> list[str]:
        request = {"parent": self.project}
        return [
            secret.name.split("/")[-1] for secret in self.client.list_secrets(request)
        ]
