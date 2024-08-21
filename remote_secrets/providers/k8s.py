from base64 import b64decode
from remote_secrets.providers.base import SecretManager

try:
    from pykube import HTTPClient, KubeConfig, Secret
    from pykube.query import Query

except ImportError:
    raise EnvironmentError('You must install \"remote-secrets[k8s]\" extras!')


class K8sSecretManager(SecretManager):

    def __init__(self, namespace: str = 'default') -> None:
        self.namespace = namespace
        self.client = HTTPClient(KubeConfig.from_file())

    def secret(self, name: str) -> Query:
        return Secret.objects(self.client, self.namespace).get(name=name)
    
    def get_json(self, name: str) -> dict[str, str]:
        content = self.secret(name).obj['data']
        return {
            key: b64decode(value).decode()
            for key, value in content.items()
        }
    
    def list(self) -> list[str]:
        return [
            secret.name
            for secret in Secret.objects(self.client, self.namespace)
        ]
    