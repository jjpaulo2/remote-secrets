from remote_secrets.providers.gcp import GCPSecretManager

try:
    from typer import Typer
    from rich.console import Console

except ImportError:
    raise EnvironmentError('You must install \"remote-secrets[cli]\" extras!')


console = Console()
secrets = GCPSecretManager()
cli = Typer(
    name='gcp',
    help='Manage GCP secrets'
)


@cli.command()
def get(name: str):
    '''Gets a value of parameter'''
    return console.print(secrets.get(name))


@cli.command()
def list():
    '''Lists all available parameters'''
    for secret in secrets.list():
        console.print(secret)


@cli.command()
def export(prefix: str = '', suffix: str = ''):
    '''Exports all secrets in .env format'''
    for s in secrets.list():
        secret_name = s.split('/')[-1]
        if secret_name.startswith(prefix) and s.endswith(suffix):
            console.print(f'{secret_name}=\'{secrets.get(secret_name)}\'')
