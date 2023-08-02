from nonebot import require
from nonebot.plugin import PluginMetadata

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")
from arclet.alconna.core import Alconna
from arclet.alconna.typing import CommandMeta
from arclet.alconna.manager import command_manager
from nonebot_plugin_alconna import on_alconna
from nonebot_plugin_saa import MessageFactory


__sora_plugin_meta__ = PluginMetadata(
    name="帮助",
    description="获取帮助",
    usage="/帮助",
    extra={"author": "KomoriDev", "priority": 5},
)


help = on_alconna(
    Alconna(
        "帮助",
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
)


@help.handle()
async def help_():
    cmds = list(filter(lambda x: not x.meta.hide, command_manager.get_commands()))
    command_string = "\n".join(
        (
            f"| {index} | {slot.name.replace('|', '&#124;').replace('[', '&#91;')} | "
            f"{slot.meta.description} | {slot.meta.usage.splitlines()[0] if slot.meta.usage else None} |"
        )
        for index, slot in enumerate(cmds)
    )
    await MessageFactory(command_string).send(at_sender=True)
    await help.finish()
