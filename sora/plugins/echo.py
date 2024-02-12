from nonebot import require

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import funcommand

from sora.permission import ADMIN, HELPER


@funcommand(permission=ADMIN | HELPER)
async def echo(msg: str):
    return msg
