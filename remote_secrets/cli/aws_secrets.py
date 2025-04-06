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
