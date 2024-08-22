from contextlib import suppress

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


@cli.command('get')
def get_any(name: str):
    '''[Shortcut] Gets a value of an AWS secret or parameter'''
    from remote_secrets.providers.aws import AWSParameterStoreManager, AWSSecretManager
    parameters = AWSParameterStoreManager()
    secrets = AWSSecretManager()

    with suppress(secrets.client.exceptions.ResourceNotFoundException):
        return console.print(secrets.get(name))
    with suppress(parameters.client.exceptions.ParameterNotFound):
        return console.print(parameters.get(name))
    console.print(f'No one parameter or secret called "{name}" was found!', style='red')
    raise Exit(22)


@cli_secrets.command('get')
def get_secret(name: str):
    '''Gets a value of secret'''
    from remote_secrets.providers.aws import AWSSecretManager
    secrets = AWSSecretManager()

    try:
        return console.print(secrets.get(name))
    except secrets.client.exceptions.ResourceNotFoundException:
        console.print(f'No one secret called "{name}" was found!', style='red')
        raise Exit(22)
    

@cli_parameters.command('get')
def get_parameter(name: str):
    '''Gets a value of parameter'''
    from remote_secrets.providers.aws import AWSParameterStoreManager
    parameters = AWSParameterStoreManager()

    try:
        return console.print(parameters.get(name))
    except parameters.client.exceptions.ParameterNotFound:
        console.print(f'No one parameter called "{name}" was found!', style='red')
        raise Exit(22)


@cli_secrets.command('list')
def list_secrets():
    '''Lists all available secrets'''
    from remote_secrets.providers.aws import AWSSecretManager
    secrets = AWSSecretManager()

    for secret in secrets.list():
        console.print(secret)
    

@cli_parameters.command('list')
def list_parameters():
    '''Lists all available parameters'''
    from remote_secrets.providers.aws import AWSParameterStoreManager
    parameters = AWSParameterStoreManager()

    for parameter in parameters.list():
        console.print(parameter)


@cli_secrets.command('export')
def export_secrets(prefix: str = '', remove_prefix: bool = False, suffix: str = '', remove_suffix: bool = False):
    '''Exports all secrets in .env format'''
    from remote_secrets.providers.aws import AWSSecretManager
    secrets = AWSSecretManager()

    for s in secrets.list():
        if s.startswith(prefix) and s.endswith(suffix):
            if remove_prefix:
                s = s.lstrip(prefix)
            if remove_suffix:
                s = s.rstrip(suffix)
            console.print(f'{s}=\'{secrets.get(s)}\'')


@cli_parameters.command('export')
def export_parameters(prefix: str = '', remove_prefix: bool = False, suffix: str = '', remove_suffix: bool = False):
    '''Exports all secrets in .env format'''
    from remote_secrets.providers.aws import AWSParameterStoreManager
    parameters = AWSParameterStoreManager()
    
    for p in parameters.list():
        if p.startswith(prefix) and p.endswith(suffix):
            if remove_prefix:
                p = p.lstrip(prefix)
            if remove_suffix:
                p = p.rstrip(suffix)
            console.print(f'{p}=\'{parameters.get(p)}\'')
