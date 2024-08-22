from contextlib import suppress
from remote_secrets.providers.aws import AWSParameterStoreManager, AWSSecretManager

try:
    from typer import Typer, Exit
    from rich.console import Console

except ImportError:
    raise EnvironmentError('You must install \"remote-secrets[cli]\" extras!')


cli = Typer(
    name='aws',
    help='Manage AWS secrets and parameters'
)
cli_secrets = Typer(
    name='secrets',
    help='Interact with AWS Secrets Manager'
)
cli_parameters = Typer(
    name='parameters',
    help='Interact with AWS Parameter Store'
)

console = Console()
parameters = AWSParameterStoreManager()
secrets = AWSSecretManager()


@cli.command('get')
def get_any(name: str):
    '''[Shortcut] Gets a value of an AWS secret or parameter'''
    with suppress(secrets.client.exceptions.ResourceNotFoundException):
        return console.print(secrets.get(name))
    with suppress(parameters.client.exceptions.ParameterNotFound):
        return console.print(parameters.get(name))
    console.print(f'No one parameter or secret called "{name}" was found!', style='red')
    raise Exit(22)


@cli_secrets.command('get')
def get_secret(name: str):
    '''Gets a value of secret'''
    try:
        return console.print(secrets.get(name))
    except secrets.client.exceptions.ResourceNotFoundException:
        console.print(f'No one secret called "{name}" was found!', style='red')
        raise Exit(22)
    

@cli_parameters.command('get')
def get_parameter(name: str):
    '''Gets a value of parameter'''
    try:
        return console.print(secrets.get(name))
    except secrets.client.exceptions.ResourceNotFoundException:
        console.print(f'No one parameter called "{name}" was found!', style='red')
        raise Exit(22)


@cli_secrets.command('list')
def list_secrets():
    '''Lists all available secrets'''
    for secret in secrets.list():
        console.print(secret)
    

@cli_parameters.command('list')
def list_parameters():
    '''Lists all available parameters'''
    for parameter in parameters.list():
        console.print(parameter)


@cli_secrets.command('export')
def export_secrets(prefix: str = '', suffix: str = ''):
    '''Exports all secrets in .env format'''
    for s in secrets.list():
        if s.startswith(prefix) and s.endswith(suffix):
            console.print(f'{s}=\'{secrets.get(s)}\'')


@cli_parameters.command('export')
def export_parameters(prefix: str = '', suffix: str = ''):
    '''Exports all secrets in .env format'''
    for p in parameters.list():
        if p.startswith(prefix) and p.endswith(suffix):
            console.print(f'{p}=\'{parameters.get(p)}\'')
