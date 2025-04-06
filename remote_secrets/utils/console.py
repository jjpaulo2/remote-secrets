from remote_secrets.providers._base import SecretManager

try:
    from rich.console import Console

except ImportError:
    raise EnvironmentError('You must install "remote-secrets[cli]" extras!')


_console = Console()


def print(obj: object):
    return _console.print(obj)


def error(message: str):
    return _console.print(message, style="red")


def dot_env(
    secret_manager: SecretManager,
    prefix: str = "",
    remove_prefix: bool = False,
    suffix: str = "",
    remove_suffix: bool = False,
):
    for s in secret_manager.list():
        secret_name = s.split("/")[-1]
        if secret_name.startswith(prefix) and s.endswith(suffix):
            secret_value = secret_manager.get(secret_name).replace("\n", "\\n")
            if remove_prefix:
                secret_name = secret_name[len(prefix) :]
            if remove_suffix:
                secret_name = secret_name[: len(suffix)]
            _console.print(f"{secret_name}='{secret_value}'")
