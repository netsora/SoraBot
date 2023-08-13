from nonebot import require

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")

from arclet.alconna.core import Alconna
from arclet.alconna.typing import CommandMeta
from nonebot_plugin_alconna import on_alconna
from nonebot_plugin_saa import Image, MessageFactory

from sora.log import logger

URL = "https://picture.yinux.workers.dev"

cos = on_alconna(
    Alconna(
        "cos",
        meta=CommandMeta(
            description="三次元也不戳，嘿嘿嘿",
            usage="/cos",
            example="/cos",
            compact=True,
        ),
    ),
    aliases={"coser"},
    priority=50,
    block=True,
)


@cos.handle()
async def cos_():
    try:
        await MessageFactory([Image(URL)]).send(at_sender=True)
    except Exception as e:
        logger.error("cos", f"{e}")
        await MessageFactory("你cos给我看！").send(at_sender=True)
    await cos.finish()
