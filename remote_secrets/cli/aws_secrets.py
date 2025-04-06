from remote_secrets.exceptions import SecretNotFoundException
from remote_secrets.providers.aws import AWSSecretManager

try:
    from typer import Typer, Exit
    from remote_secrets.utils import console

except ImportError:
    raise EnvironmentError('You must install "remote-secrets[cli]" extras!')


cli = Typer(name="secrets", help="Interact with AWS Secrets Manager")


@cli.command()
def get(name: str, region: str | None = None):
    """Gets a value of secret"""
    secrets = AWSSecretManager(region)
    try:
        return console.print(secrets.get(name))
    except SecretNotFoundException:
        console.error(f'No one secret called "{name}" was found!')
        raise Exit(22)


@cli.command()
def update(name: str, value: str, region: str | None = None):
    """Updates a secret with a new value"""
    secrets = AWSSecretManager(region)
    secrets.update(name, value)


@cli.command()
def create(name: str, value: str, region: str | None = None):
    """Creates a secret with the given name and value"""
    secrets = AWSSecretManager(region)
    secrets.create(name, value)


@cli.command()
def delete(name: str, region: str | None = None):
    """Deletes a given secret"""
    secrets = AWSSecretManager(region)
    secrets.delete(name)


@cli.command()
def list(region: str | None = None):
    """Lists all available secrets"""
    secrets = AWSSecretManager(region)
    for secret in secrets.list():
        console.print(secret)


@cli.command()
def export(
    prefix: str = "",
    remove_prefix: bool = False,
    suffix: str = "",
    remove_suffix: bool = False,
    region: str | None = None,
):
    """Exports all secrets in .env format"""
    secrets = AWSSecretManager(region)
    console.dot_env(
        secrets,
        prefix=prefix,
        remove_prefix=remove_prefix,
        suffix=suffix,
        remove_suffix=remove_suffix,
    )
