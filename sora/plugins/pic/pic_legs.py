from nonebot import require

from sora.utils.requests import AsyncHttpx

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")

from arclet.alconna.core import Alconna
from arclet.alconna.typing import CommandMeta
from nonebot_plugin_alconna import on_alconna
from nonebot_plugin_saa import Image, MessageFactory

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
    aliases={"看腿"},
    priority=50,
    block=True,
)


@legs.handle()
async def legs_():
    res = await AsyncHttpx.get(URL)
    data = res.text.strip()
    await MessageFactory([Image(data)]).send(at_sender=True)
    await legs.finish()
