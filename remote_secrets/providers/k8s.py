from base64 import b64decode, b64encode
from remote_secrets.exceptions import SecretNotFoundException
from remote_secrets.providers._base import SecretManager

try:
    from pykube import HTTPClient, KubeConfig, Secret
    from pykube.exceptions import ObjectDoesNotExist

except ImportError:
    raise EnvironmentError('You must install "remote-secrets[k8s]" extras!')


class K8sSecretManager(SecretManager):
    client: HTTPClient

    def __init__(self, namespace: str = "default"):
        self.namespace = namespace
        self.client = HTTPClient(KubeConfig.from_file())

    def _encode(self, value: dict[str, str]) -> dict[str, str]:
        encoded = value.copy()
        for key in encoded.keys():
            encoded[key] = b64encode(encoded[key].encode()).decode()
        return encoded

    def _decode(self, value: dict[str, str]) -> dict[str, str]:
        decoded = value.copy()
        for key in decoded.keys():
            decoded[key] = b64decode(decoded[key]).decode()
        return decoded

    def secret(self, name: str) -> Secret:
        try:
            return Secret.objects(self.client, self.namespace).get(name=name)
        except ObjectDoesNotExist:
            raise SecretNotFoundException(name)

    def get_json(self, name: str) -> dict[str, str]:
        return self._decode(self.secret(name).obj["data"])

    def update_json(self, name: str, value: dict[str, str]):
        secret = self.secret(name)
        secret.obj["data"] = self._encode(value)
        secret.update()

    def create_json(self, name: str, value: dict[str, str], **kwargs):
        secret = Secret(
            api=self.client,
            obj={
                "apiVersion": "v1",
                "kind": "Secret",
                "metadata": {"name": name, "namespace": self.namespace},
                "type": "Opaque",
                "data": self._encode(value),
            },
        )
        secret.create()

    def delete(self, name: str, **kwargs):
        self.secret(name).delete()

    def list(self) -> list[str]:
        return [secret.name for secret in Secret.objects(self.client, self.namespace)]
