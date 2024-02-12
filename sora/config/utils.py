import importlib
import itertools
from typing import Any
from pathlib import Path
from collections.abc import Callable

from nonebot.plugin import Plugin

try:  # pragma: py-gte-311
    import tomllib  # pyright: ignore[reportMissingImports]
except ModuleNotFoundError:  # pragma: py-lt-311
    import tomli as tomllib


def load_config() -> dict[str, Any]:
    """
    加载配置。
    """

    def load_file(path: str | Path) -> dict[str, Any]:
        return tomllib.loads(Path(path).read_text(encoding="utf-8"))

    file_name = ("sora", "sora.config")
    file_type = ("toml", "yaml", "yml", "json")
    config_files = itertools.product(file_name, file_type)
    for name, type in config_files:
        file = Path(f"{name}.{type}")
        if file.is_file():
            return load_file(file)
    pyproject = load_file("pyproject.toml")
    return pyproject.get("tool", {}).get("sora", {})


def find_plugin(cls: Callable[..., Any], /) -> Plugin | None:
    """查找类所在的插件对象

    ### 参数
        cls: 查找的类
    """
    module_name = cls.__module__
    module = importlib.import_module(module_name)
    parts = module_name.split(".")

    for i in range(len(parts), 0, -1):
        current_module = ".".join(parts[:i])
        module = importlib.import_module(current_module)
        if plugin := getattr(module, "__plugin__", None):
            return plugin

    return None
