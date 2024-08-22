from remote_secrets.cli import aws
from remote_secrets.cli import gcp
from typer import Typer

aws.cli.add_typer(aws.cli_secrets)
aws.cli.add_typer(aws.cli_parameters)

cli = Typer()
cli.add_typer(aws.cli)
cli.add_typer(gcp.cli)

if __name__ == '__main__':
    cli()
