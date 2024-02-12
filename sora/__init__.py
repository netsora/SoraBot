import importlib
from pathlib import Path
from typing import Any, ClassVar

import nonebot
from nonebot.plugin import Plugin
from nonebot.drivers import Driver
from nonebot.utils import path_to_module_name
from nonebot.plugin.manager import PluginManager, _managers

from .log import console
from .hook import install_hook
from .log import logger as logger
from .log import Text, Panel, Columns
from .version import __version__, __metadata__
from .config import bot_config, sora_config, plugin_config


class SoraBot:
    driver: ClassVar[Driver]

    def __init__(self) -> None:
        self.show_logo()

        if bot_config.debug:
            self.print_environment()
            console.rule()

        self.init_nonebot(_mixin_config(bot_config.dict()))

        logger.opt(colors=True).success("🚀 <y><b>SoraBot is initializing...</b></y>")

        logger.opt(colors=True).debug(
            f"Loaded <y><b>Config</b></y>: {sora_config.dict()}"
        )

        self.load_plugins()

        install_hook()

        logger.opt(colors=True).success("🚀 <y><b>SoraBot is Running...</b></y>")

        if bot_config.debug:
            console.rule("[blink][yellow]当前处于调试模式中, 请勿在生产环境打开[/][/]")

    def run(self, *args, **kwargs) -> None:
        """Sora，启动！"""
        self.driver.run(*args, **kwargs)

    def init_nonebot(self, config: dict[str, Any]) -> None:
        """初始化 NoneBot"""
        nonebot.init(**config)

        self.__class__.driver = nonebot.get_driver()
        self.load_adapters(config["adapters"])

    def load_adapters(self, adapters: set[str]) -> None:
        """加载适配器"""
        adapters = {adapter.replace("~", "nonebot.adapters.") for adapter in adapters}
        for adapter in adapters:
            module = importlib.import_module(adapter)
            self.driver.register_adapter(getattr(module, "Adapter"))

    def load_plugins(self) -> None:
        """加载插件"""
        plugins = {
            path_to_module_name(pp) if (pp := Path(p)).exists() else p
            for p in plugin_config.plugins
        }
        manager = PluginManager(plugins, plugin_config.plugin_dirs)
        plugins = manager.available_plugins
        _managers.append(manager)

        if plugin_config.whitelist:
            plugins &= plugin_config.whitelist

        if plugin_config.blacklist:
            plugins -= plugin_config.blacklist

        loaded_plugins = set(
            filter(None, (manager.load_plugin(name) for name in plugins))
        )

        self.loading_state(loaded_plugins)

    def loading_state(self, plugins: set[Plugin]) -> None:
        """打印插件加载状态"""
        if loaded_plugins := nonebot.get_loaded_plugins():
            logger.opt(colors=True).info(
                f"✅ [magenta]Total {len(loaded_plugins)} plugin are successfully loaded.[/]"
            )

        if failed_plugins := plugins - loaded_plugins:
            logger.opt(colors=True).error(
                f"❌ [magenta]Total {len(failed_plugins)} plugin are failed loaded.[/]: {', '.join(plugin.name for plugin in failed_plugins)}"  # noqa: E501
            )

    def show_logo(self) -> None:
        """打印 LOGO"""
        console.print(
            Columns(
                [Text(LOGO.lstrip("\n"), style="bold blue")],
                align="center",
                expand=True,
            )
        )

    def print_environment(self) -> None:
        """打印环境信息"""
        import platform

        environment_info = {
            "OS": platform.system(),
            "Arch": platform.machine(),
            "Python": platform.python_version(),
            "SoraBot": __version__,
            "NoneBot": nonebot.__version__,
        }

        renderables = [
            Panel(
                Text(justify="center")
                .append(k, style="bold")
                .append(f"\n{v}", style="yellow"),
                expand=True,
                width=console.size.width // 6,
            )
            for k, v in environment_info.items()
        ]
        console.print(
            Columns(
                renderables,
                align="center",
                title="Environment Info",
                expand=True,
                equal=True,
            )
        )


def get_driver() -> Driver:
    """
    获取全局 `Driver` 实例。
    """
    if SoraBot.driver is None:
        raise ValueError("SoraBot has not been initialized.")
    return SoraBot.driver


def _mixin_config(config: dict[str, Any]) -> dict[str, Any]:
    if config["debug"]:
        config |= {
            "fastapi_openapi_url": config.get("fastapi_openapi_url", "/openapi.json"),
            "fastapi_docs_url": config.get("fastapi_docs_url", "/docs"),
            "fastapi_redoc_url": config.get("fastapi_redoc_url", "/redoc"),
        }
    config["fastapi_extra"] = {
        "title": __metadata__.name,
        "version": __metadata__.version,
        "description": __metadata__.summary,
    }

    return config


LOGO = r"""
   _____                     ____        __
  / ___/____  _________ _   / __ )____  / /_
  \__ \/ __ \/ ___/ __ `/  / __  / __ \/ __/
 ___/ / /_/ / /  / /_/ /  / /_/ / /_/ / /_
/____/\____/_/   \__,_/  /_____/\____/\__/
"""
