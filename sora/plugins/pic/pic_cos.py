from nonebot import require

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")

from nonebot_plugin_saa import Text, Image
from nonebot_plugin_alconna import Alconna, CommandMeta, on_alconna

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
    priority=50,
    block=True,
)
cos.shortcut("coser", prefix=True)


@cos.handle()
async def _():
    try:
        await Image(URL).send(at_sender=True)
    except Exception as e:
        logger.error(f"{e}")
        await Text("你cos给我看！").send(at_sender=True)
    await cos.finish()
