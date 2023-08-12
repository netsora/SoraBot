import yaml
from pathlib import Path
from typing import Any

from sora.log import logger


class Config:
    def __init__(
        self,
        value: Any,
        name: str | None = None,
        help: str | None = None,
        options: list[str] | None = None,
    ):
        self.value = value
        self.name = name
        self.help = help
        self.options = options


class ConfigsManager:
    """
    配置管理器
    """

    def __init__(self, file: Path):
        self._data: dict[str, dict[str, Config]] = {}
        self.file = file

        self.file.parent.mkdir(parents=True, exist_ok=True)
        if self.file.exists():
            self.load()
        else:
            self.save()

    def add_config(
        self,
        module: str,
        key: str,
        value: Any,
        name: str | None = None,
        help: str | None = None,
        options: list[str] | None = None,
    ):
        """
        说明：
            增加配置
        参数：
            * module: 模块
            * key: 键
            * value: 值
            * name
            * help: 注解
            * options: 配置选项"""
        if module not in self._data:
            self._data[module] = {}
        self._data[module][key] = Config(
            value=value, name=name, help=help, options=options
        )
        self.save()

    def set_config(self, module: str, key: str, value: Any):
        """
        说明：
            设置配置
        参数：
            * module: 模块
            * key: 键
            * value: 值
        """
        if module in self._data and key in self._data[module]:
            self._data[module][key].value = value
            self.save()

    def get_config(self, module: str, key: str, default=None) -> Any:
        """
        说明：
            获取配置值
        参数：
            * module: 模块
            * key: 键
            * default: 默认值（若value为None，则返回default）"""
        if module in self._data and key in self._data[module]:
            return self._data[module][key].value
        return default

    def save(self):
        data = {
            module: {
                key: {
                    "value": config.value,
                    "name": config.name,
                    "help": config.help,
                    "options": config.options,
                }
                for key, config in configs.items()
            }
            for module, configs in self._data.items()
        }
        with open(self.file, "w", encoding="utf8") as f:
            yaml.dump(data, f, indent=2, allow_unicode=True)

    def load(self):
        with open(self.file, encoding="utf8") as f:
            data = yaml.safe_load(f)

        if data is None:
            logger.error("配置管理器", f"无效或空的配置文件：{self.file}")
            return

        for module, configs in data.items():
            if module not in self._data:
                self._data[module] = {}
            for key, config_data in configs.items():
                value = config_data.get("value")
                name = config_data.get("name")
                help = config_data.get("help")
                options = config_data.get("options")
                self._data[module][key] = Config(
                    value=value, name=name, help=help, options=options
                )
