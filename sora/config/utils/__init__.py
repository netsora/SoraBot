from ruamel import yaml
from ruamel.yaml import YAML

from sora.log import logger
from sora.config.path import SORA_CONFIG


class ConfigManager:
    config_path = SORA_CONFIG

    @classmethod
    def init(cls):
        logger.success("配置管理器", "<g>初始化完成</g>")

    @classmethod
    def load_config(cls):
        with open(cls.config_path, encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return config

    @classmethod
    def save_config(cls, config):
        yaml = YAML()
        yaml.dump(config, open(cls.config_path, "w", encoding="utf-8"))

    @classmethod
    def set_config(cls, key, value):
        config = cls.load_config()
        keys = key.split(".")
        nested_config = config
        for k in keys[:-1]:
            nested_config = nested_config.get(k, {})
        if keys[-1] not in nested_config:
            raise ValueError(f'配置项 "{key}" 不存在')
        nested_config[keys[-1]] = value
        cls.save_config(config)

    @classmethod
    def add_config(cls, key, value):
        config = cls.load_config()
        keys = key.split(".")
        nested_config = config
        for k in keys[:-1]:
            nested_config = nested_config.setdefault(k, {})
        if keys[-1] in nested_config:
            raise ValueError(f'配置项 "{key}" 已存在')
        nested_config[keys[-1]] = value
        cls.save_config(config)

    @classmethod
    def get_config(cls, key):
        config = cls.load_config()
        keys = key.split(".")
        nested_config = config
        for k in keys:
            nested_config = nested_config.get(k, {})
        return nested_config
