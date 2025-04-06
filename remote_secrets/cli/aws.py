from contextlib import suppress

from remote_secrets.exceptions import SecretNotFoundException
from remote_secrets.providers.aws import AWSParameterStoreManager, AWSSecretManager

try:
    from typer import Typer, Exit
    from remote_secrets.utils import console

except ImportError:
    raise EnvironmentError('You must install "remote-secrets[cli]" extras!')


cli = Typer(name="aws", help="Manage AWS secrets and parameters")


@cli.command("get")
def get_any(name: str):
    """[Shortcut] Gets a value of an AWS secret or parameter"""
    parameters = AWSParameterStoreManager()
    secrets = AWSSecretManager()

    with suppress(SecretNotFoundException):
        return console.print(secrets.get(name))

    with suppress(SecretNotFoundException):
        return console.print(parameters.get(name))

    console.error(f'No one parameter or secret called "{name}" was found!')
    raise Exit(22)
