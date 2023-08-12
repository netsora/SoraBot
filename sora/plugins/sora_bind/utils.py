import toml

from typing import Any
from pathlib import Path


async def update_toml_file(file_path: Path, key: str, value: Any, module=None):
    with open(file_path) as file:
        data = toml.load(file)

    if module is not None:
        data[module][key] = value
    else:
        data[key] = value

    with open(file_path, "w") as file:
        toml.dump(data, file)


async def read_value(file_path: Path, key: str, module=None):
    with open(file_path) as file:
        data = toml.load(file)

    if module is not None:
        value = data[module][key]
    else:
        value = data[key]

    return value
