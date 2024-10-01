from typing import TypeVar

PythonTypes = str | float | int | bool | type
CastType = TypeVar("CastType", bound=PythonTypes)
