from nonebot import require

from sora.utils.requests import AsyncHttpx

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")

from nonebot_plugin_saa import Image
from arclet.alconna.core import Alconna
from arclet.alconna.typing import CommandMeta
from nonebot_plugin_alconna import on_alconna

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
    priority=50,
    block=True,
)
jk.shortcut("看裙", prefix=True)


@jk.handle()
async def _():
    res = await AsyncHttpx.get(URL)
    data = res.text.strip()
    await Image(data).finish(at_sender=True)
