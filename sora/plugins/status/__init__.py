"""运行状态"""

from nonebot import require
from nonebot.rule import to_me

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import Command
from nonebot_plugin_alconna.uniseg import UniMessage

from .drawer import draw

status = (
    Command("status", help_text="查看林汐运行状态")
    .usage("@bot /status\n@bot /状态")
    .action(lambda: UniMessage.image(raw=draw()))
    .build(rule=to_me())
)
status.shortcut("状态", {"prefix": True})
status.shortcut("运行状态", {"prefix": True})
