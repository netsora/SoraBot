from nonebot import require

from sora.utils.requests import AsyncHttpx

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")

from nonebot_plugin_saa import Image
from arclet.alconna.core import Alconna
from arclet.alconna.typing import CommandMeta
from nonebot_plugin_alconna import on_alconna

URL = "http://81.70.100.130/api/tu.php"

legs = on_alconna(
    Alconna(
        "玉足",
        meta=CommandMeta(
            description="什么都玉足只会害了你",
            usage="/玉足",
            example="/玉足",
            compact=True,
        ),
    ),
    priority=50,
    block=True,
)
legs.shortcut("看腿", prefix=True)


@legs.handle()
async def _():
    res = await AsyncHttpx.get(URL)
    data = res.text.strip()
    await Image(data).finish(at_sender=True)
