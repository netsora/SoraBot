from nonebot import require
from nonebot.rule import to_me

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")
from arclet.alconna.args import Args
from arclet.alconna.core import Alconna
from arclet.alconna.typing import CommandMeta
from arclet.alconna.manager import command_manager
from nonebot_plugin_alconna import Match, on_alconna, AlconnaMatch
from nonebot_plugin_saa import MessageFactory


help = on_alconna(
    Alconna(
        "帮助",
        Args["plugin?", str],
        meta=CommandMeta(
            description="获取林汐帮助文档",
            usage="@bot /帮助",
            example="@bot /帮助",
            compact=True,
        ),
    ),
    aliases={"help"},
    priority=5,
    block=True,
    rule=to_me(),
)


@help.handle()
async def help_(plugin: Match[str] = AlconnaMatch("plugin")):
    if plugin.available:
        plugin_help = command_manager.command_help(plugin.result)
        if plugin_help is None:
            await MessageFactory("唔...没有找到帮助呢").send(at_sender=True)
            await help.finish()
        await MessageFactory(plugin_help).send(at_sender=True)
        await help.finish()

    await MessageFactory(command_manager.all_command_help()).send(at_sender=True)
    await help.finish()
