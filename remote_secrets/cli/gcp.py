try:
    from typer import Typer
    from rich.console import Console

except ImportError:
    raise EnvironmentError('You must install \"remote-secrets[cli]\" extras!')


console = Console()
cli = Typer(
    name='gcp',
    help='Manage GCP secrets'
)


@cli.command()
def get(name: str):
    '''Gets a value of parameter'''
    from remote_secrets.providers.gcp import GCPSecretManager
    secrets = GCPSecretManager()

    return console.print(secrets.get(name))


@cli.command()
def list():
    '''Lists all available parameters'''
    from remote_secrets.providers.gcp import GCPSecretManager
    secrets = GCPSecretManager()

    for secret in secrets.list():
        console.print(secret)


@cli.command()
def export(prefix: str = '', remove_prefix: bool = False, suffix: str = '', remove_suffix: bool = False):
    '''Exports all secrets in .env format'''
    from remote_secrets.providers.gcp import GCPSecretManager
    secrets = GCPSecretManager()
    
    for s in secrets.list():
        secret_name = s.split('/')[-1]
        if secret_name.startswith(prefix) and s.endswith(suffix):
            secret_value = secrets.get(secret_name).replace('\n', '\\n')
            if remove_prefix:
                secret_name = secret_name[len(prefix):]
            if remove_suffix:
                secret_name = secret_name[:len(suffix)]
            console.print(f'{secret_name}=\'{secret_value}\'')
