from nonebot import require

from sora.utils.requests import AsyncHttpx

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")

from arclet.alconna.core import Alconna
from arclet.alconna.typing import CommandMeta
from nonebot_plugin_alconna import on_alconna
from nonebot_plugin_saa import Image, MessageFactory

URL = "https://api.sevin.cn/api/jk.php"

jk = on_alconna(
    Alconna(
        "jk",
        meta=CommandMeta(
            description="谁不喜欢看Jk呢？",
            usage="/jk",
            example="/jk",
            compact=True,
        ),
    ),
    aliases={"看裙"},
    priority=50,
    block=True,
)


@jk.handle()
async def jk_():
    res = await AsyncHttpx.get(URL)
    data = res.text.strip()
    await MessageFactory([Image(data)]).send(at_sender=True)
    await jk.finish()
