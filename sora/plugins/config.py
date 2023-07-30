try:
    import ujson as json
except ImportError:
    import json

from typing import Any

from nonebot import require
from nonebot.rule import to_me
from nonebot.plugin import PluginMetadata

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")
from arclet.alconna.args import Args
from arclet.alconna.core import Alconna
from arclet.alconna.typing import CommandMeta
from nonebot_plugin_saa import MessageFactory
from nonebot_plugin_alconna import Match, AlconnaMatch, on_alconna

from sora.config import ConfigManager
from sora.permission import BOT_ADMIN, BOT_HELPER

__plugin_meta__ = PluginMetadata(
    name="Config",
    description="使用指令来修改林汐配置",
    usage="/读取配置 <键>\n/增加配置 <键> <值>\n/设置配置 <键> <值>",
    extra={"author": "KomoriDev", "priority": 5},
)


getConfig = on_alconna(
    Alconna(
        "读取配置",
        Args["config", str],
        meta=CommandMeta(
            description="读取林汐配置项",
            usage="@bot /读取配置 <键>",
            example="@bot /读取配置 Login",
            compact=True,
        ),
    ),
    priority=5,
    block=True,
    rule=to_me(),
    permission=BOT_HELPER,
)

addConfig = on_alconna(
    Alconna(
        "增加配置",
        Args["key", str]["value", Any],
        meta=CommandMeta(
            description="增加林汐配置项",
            usage="@bot /增加配置 <键> <值>",
            example="@bot /增加配置 <键> <值>",
            compact=True,
        ),
    ),
    priority=5,
    block=True,
    rule=to_me(),
    permission=BOT_ADMIN,
)

setConfig = on_alconna(
    Alconna(
        "设置配置",
        Args["key", str]["value", Any],
        meta=CommandMeta(
            description="设置林汐配置项",
            usage="@bot /设置配置 <键> <值>",
            example="@bot /增加配置 <键> <值>",
            compact=True,
        ),
    ),
    aliases={"修改配置"},
    priority=5,
    block=True,
    rule=to_me(),
    permission=BOT_ADMIN,
)


@getConfig.handle()
async def get_(config: Match[str] = AlconnaMatch("config")):
    key = config.result
    value = ConfigManager.get_config(key)
    value = json.dumps(value, indent=4)
    if value is not None:
        await MessageFactory(f"配置项 {key} 的值为 {value}").send(at_sender=True)
        await getConfig.finish()
    else:
        await MessageFactory(f"配置项 {key} 不存在").send(at_sender=True)
        await getConfig.finish()


@addConfig.handle()
async def add_(
    config_key: Match[str] = AlconnaMatch("key"),
    config_value: Match[Any] = AlconnaMatch("value"),
):
    key = config_key.result
    value = config_value.result
    try:
        ConfigManager.add_config(key, value)
        await MessageFactory("配置项增加成功！").send(at_sender=True)
        await addConfig.finish()
    except ValueError as e:
        await MessageFactory(str(e)).send(at_sender=True)
        await addConfig.finish()


@setConfig.handle()
async def set_(
    config_key: Match[str] = AlconnaMatch("key"),
    config_value: Match[Any] = AlconnaMatch("value"),
):
    key = config_key.result
    value = config_value.result
    try:
        ConfigManager.set_config(key, value)
        await MessageFactory("配置项设置成功！").send(at_sender=True)
        await setConfig.finish()
    except ValueError as e:
        await MessageFactory(str(e)).send(at_sender=True)
        await setConfig.finish()
