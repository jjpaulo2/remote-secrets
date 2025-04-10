from remote_secrets.providers.k8s import K8sSecretManager

try:
    from typer import Typer
    from remote_secrets.utils import console

except ImportError:
    raise EnvironmentError('You must install "remote-secrets[k8s]" extras!')


cli = Typer(name="gcp", help="Manage Kubernetes secrets")


@cli.command()
def get(name: str, namespace: str = 'default'):
    """Gets a value of secret"""
    secrets = K8sSecretManager(namespace)
    return console.print(secrets.get(name))


@cli.command()
def update(name: str, value: str, namespace: str = 'default'):
    """Updates a secret with a new value"""
    secrets = K8sSecretManager(namespace)
    secrets.update(name, value)


@cli.command()
def create(name: str, value: str, namespace: str = 'default'):
    """Creates a secret with the given name and value"""
    secrets = K8sSecretManager(namespace)
    secrets.create(name, value)


@cli.command()
def delete(name: str, namespace: str = 'default'):
    """Deletes a given secret"""
    secrets = K8sSecretManager(namespace)
    secrets.delete(name)


@cli.command()
def list(namespace: str = 'default'):
    """Lists all available secrets"""
    secrets = K8sSecretManager(namespace)
    for secret in secrets.list():
        console.print(secret)


# @cli.command()
# def export(
#     prefix: str = "",
#     remove_prefix: bool = False,
#     suffix: str = "",
#     remove_suffix: bool = False,
#     namespace: str = 'default',
# ):
#     """Exports all secrets in .env format"""
#     secrets = K8sSecretManager(namespace)
#     console.dot_env(
#         secrets,
#         prefix=prefix,
#         remove_prefix=remove_prefix,
#         suffix=suffix,
#         remove_suffix=remove_suffix,
#     )
