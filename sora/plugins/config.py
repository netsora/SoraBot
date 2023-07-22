try:
    import ujson as json
except ImportError:
    import json

from nonebot.params import CommandArg
from nonebot import require, on_command
from nonebot.plugin import PluginMetadata
from nonebot.internal.adapter import Message

require("nonebot_plugin_saa")
from nonebot_plugin_saa import MessageFactory

from sora.config import ConfigManager
from sora.permission import BOT_ADMIN, BOT_HELPER

__plugin_meta__ = PluginMetadata(
    name="Config",
    description="使用指令来修改林汐配置",
    usage="/读取配置 <键>\n/增加配置 <键> <值>\n/设置配置 <键> <值>",
    extra={"author": "KomoriDev", "priority": 5},
)


getConfig = on_command(
    cmd="读取配置",
    priority=5,
    block=True,
    permission=BOT_HELPER,
    state={
        "name": "getConfig",
        "description": "读取林汐配置项",
        "usage": "/读取配置 <键>",
        "priority": 5,
    },
)

addConfig = on_command(
    cmd="增加配置",
    priority=5,
    block=True,
    permission=BOT_ADMIN,
    state={
        "name": "addConfig",
        "description": "增加林汐配置项",
        "usage": "/增加配置 <键> <值>",
        "priority": 5,
    },
)

setConfig = on_command(
    cmd="设置配置",
    aliases={"修改配置"},
    priority=5,
    block=True,
    permission=BOT_ADMIN,
    state={
        "name": "setConfig",
        "description": "设置林汐配置项",
        "usage": "/设置配置 <键> <值>",
        "priority": 5,
    },
)


@getConfig.handle()
async def get_(msg: Message = CommandArg()):
    key = msg.extract_plain_text().strip()
    value = ConfigManager.get_config(key)
    value = json.dumps(value, indent=4)
    if value is not None:
        await MessageFactory(f"配置项 {key} 的值为 {value}").send(at_sender=True)
        await getConfig.finish()
    else:
        await MessageFactory(f"配置项 {key} 不存在").send(at_sender=True)
        await getConfig.finish()


@addConfig.handle()
async def add_(msg: Message = CommandArg()):
    message = msg.extract_plain_text().split(" ", 1)
    key = message[0]
    value = message[1]
    try:
        ConfigManager.add_config(key, value)
        await MessageFactory("配置项增加成功！").send(at_sender=True)
        await addConfig.finish()
    except ValueError as e:
        await MessageFactory(str(e)).send(at_sender=True)
        await addConfig.finish()


@setConfig.handle()
async def set_(msg: Message = CommandArg()):
    message = msg.extract_plain_text().split(" ", 1)
    key = message[0]
    value = message[1]
    try:
        ConfigManager.set_config(key, value)
        await MessageFactory("配置项设置成功！").send(at_sender=True)
        await setConfig.finish()
    except ValueError as e:
        await MessageFactory(str(e)).send(at_sender=True)
        await setConfig.finish()
