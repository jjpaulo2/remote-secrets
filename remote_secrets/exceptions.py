class MethodNotSupported(NotImplementedError):
    def __init__(self, method_name: str, class_name: str) -> None:
        self.method_name = method_name
        self.class_name = class_name
        super().__init__(
            f'Method "{method_name}" not supported for provider "{class_name}"!'
        )


class SecretNotFoundException(Exception): ...


class InvalidSecretException(Exception): ...
