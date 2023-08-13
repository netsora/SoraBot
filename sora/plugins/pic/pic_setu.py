from httpx import ConnectError

from nonebot import require

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")

from arclet.alconna.args import Args
from arclet.alconna.base import Option
from arclet.alconna.core import Alconna
from arclet.alconna.arparma import Arparma
from arclet.alconna.typing import MultiVar, CommandMeta
from nonebot_plugin_alconna import Match, on_alconna, AlconnaMatch, AlconnaMatches
from nonebot_plugin_saa import Text, Image, MessageFactory

from sora.log import logger
from sora.utils.requests import AsyncHttpx

URL: str = "https://api.lolicon.app/setu/v2?r18={r18}&tag={tag}"

setu = on_alconna(
    Alconna(
        "setu",
        Args["tag?", MultiVar(str)],
        Option("-r", Args["r18", bool, False]),
        meta=CommandMeta(
            description="谁不喜欢看色图呢？",
            usage="/setu",
            example="/色图",
            compact=True,
        ),
    ),
    aliases={"色图", "涩图"},
    priority=50,
    block=True,
)


@setu.handle()
async def setu_(
    keyword: Match[str] = AlconnaMatch("tag"), r18: Arparma = AlconnaMatches()
):
    if r18.find("r"):
        r18_result: int = 1
    else:
        r18_result: int = 0

    if keyword.available:
        tag = "|".join(keyword.result)
    else:
        tag = ""

    url = URL.format(r18=r18_result, tag=tag)
    logger.info("setu", url)
    request_json = {"tag": tag}

    try:
        res = await AsyncHttpx.post(url, json=request_json)
        parsed_data = res.json()
        title = parsed_data["data"][0]["title"]
        original_url = parsed_data["data"][0]["urls"]["original"]
        await MessageFactory([Text(title), Image(original_url)]).send(at_sender=True)
    except ConnectError:
        logger.error("setu", "网络错误")
        await MessageFactory("网络错误，再试一次叭").send(at_sender=True)
    except Exception as e:
        logger.error("setu", f"{e}")
        await MessageFactory("图片发不出去呢，只能我自己看啦").send(at_sender=True)

    await setu.finish()
