from remote_secrets.providers.gcp import GCPSecretManager

try:
    from typer import Typer
    from remote_secrets.utils import console

except ImportError:
    raise EnvironmentError('You must install "remote-secrets[cli]" extras!')


cli = Typer(name="gcp", help="Manage GCP secrets")


@cli.command()
def get(name: str, project_id: str | None = None):
    """Gets a value of secret"""
    secrets = GCPSecretManager(project_id)
    return console.print(secrets.get(name))


@cli.command()
def update(name: str, value: str, project_id: str | None = None):
    """Updates a secret with a new value"""
    secrets = GCPSecretManager(project_id)
    secrets.update(name, value)


@cli.command()
def create(name: str, value: str, project_id: str | None = None):
    """Creates a secret with the given name and value"""
    secrets = GCPSecretManager(project_id)
    secrets.create(name, value)


@cli.command()
def delete(name: str, project_id: str | None = None):
    """Deletes a given secret"""
    secrets = GCPSecretManager(project_id)
    secrets.delete(name)


@cli.command()
def list(project_id: str | None = None):
    """Lists all available secrets"""
    secrets = GCPSecretManager(project_id)
    for secret in secrets.list():
        console.print(secret)


@cli.command()
def export(
    prefix: str = "",
    remove_prefix: bool = False,
    suffix: str = "",
    remove_suffix: bool = False,
    project_id: str | None = None,
):
    """Exports all secrets in .env format"""
    secrets = GCPSecretManager(project_id)
    console.dot_env(
        secrets,
        prefix=prefix,
        remove_prefix=remove_prefix,
        suffix=suffix,
        remove_suffix=remove_suffix,
    )
