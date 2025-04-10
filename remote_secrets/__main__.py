from typer import Typer

from remote_secrets.cli import aws
from remote_secrets.cli import aws_parameters
from remote_secrets.cli import aws_secrets
from remote_secrets.cli import gcp
from remote_secrets.cli import k8s

aws.cli.add_typer(aws_parameters.cli)
aws.cli.add_typer(aws_secrets.cli)

cli = Typer()
cli.add_typer(aws.cli)
cli.add_typer(gcp.cli)
cli.add_typer(k8s.cli)

if __name__ == "__main__":
    cli()
