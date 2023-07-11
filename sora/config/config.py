from time import sleep
from pathlib import Path

import yaml
from sora.log import logger

from .create import _init_config
from .models import ConfigModel, WithGoCQHTTP, RuntimeConfig

_DEFAULT_CONFIG_PATH = Path(".") / "sora" / "config" / "default_config.yaml"


class Config:
    def __init__(self, config_path: Path):
        if not config_path.is_file():
            _init_config(config_path, _DEFAULT_CONFIG_PATH)
            sleep(3)

        raw_conf = yaml.safe_load(_DEFAULT_CONFIG_PATH.read_bytes())
        config = yaml.safe_load(config_path.read_bytes())

        if raw_conf.get("ConfigVersion") != config.get("ConfigVersion"):
            logger.warning("配置", "你的 config.yml 文件已过时")
            sleep(3)
            exit(-1)

        self.config = config

        def parse(self) -> ConfigModel:
            return ConfigModel.parse_obj(self.config)

    def parse(self) -> ConfigModel:
        return ConfigModel.parse_obj(self.config)

    def get_runtime_conf(self) -> dict:
        gocqhttp_conf = WithGoCQHTTP.parse_obj(self.config["WithGoCQHTTP"])

        return RuntimeConfig(
            gocqhttp_accounts=gocqhttp_conf.accounts,
            gocqhttp_download_domain=gocqhttp_conf.download_domain,
            gocqhttp_version=gocqhttp_conf.download_version,
            gocqhttp_webui_username=gocqhttp_conf.gocqhttp_webui_username,
            gocqhttp_webui_password=gocqhttp_conf.gocqhttp_webui_password,
        ).dict()
