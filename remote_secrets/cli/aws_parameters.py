from remote_secrets.exceptions import SecretNotFoundException
from remote_secrets.providers.aws import AWSParameterStoreManager

try:
    from typer import Typer, Exit
    from remote_secrets.utils import console

except ImportError:
    raise EnvironmentError('You must install "remote-secrets[cli]" extras!')


cli = Typer(name="parameters", help="Interact with AWS Parameter Store")


@cli.command()
def get(name: str, region: str | None = None):
    """Gets a value of parameter"""
    parameters = AWSParameterStoreManager(region)
    try:
        return console.print(parameters.get(name))
    except SecretNotFoundException:
        console.error(f'No one parameter called "{name}" was found!')
        raise Exit(22)


@cli.command()
def list(region: str | None = None):
    """Lists all available parameters"""
    parameters = AWSParameterStoreManager(region)
    for parameter in parameters.list():
        console.print(parameter)


@cli.command()
def export(
    prefix: str = "",
    remove_prefix: bool = False,
    suffix: str = "",
    remove_suffix: bool = False,
    region: str | None = None,
):
    """Exports all secrets in .env format"""
    parameters = AWSParameterStoreManager(region)
    console.dot_env(
        parameters,
        prefix=prefix,
        remove_prefix=remove_prefix,
        suffix=suffix,
        remove_suffix=remove_suffix,
    )
