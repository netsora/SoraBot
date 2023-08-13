try:
    import ujson as json
except ImportError:
    import json

import base64
import random
import string
from io import BytesIO
from typing import cast, TypedDict

from PIL import Image
from websockets.client import connect
from httpx._exceptions import NetworkError

from nonebot import require
from nonebot.typing import T_State
from nonebot.adapters.qqguild import Bot as GuildBot
from nonebot.adapters.onebot.v11 import Bot as V11Bot
from nonebot.adapters.telegram.bot import Bot as TGBot
from nonebot.adapters.onebot.v11 import MessageEvent as V11MessageEvent
from nonebot.adapters.qqguild import MessageEvent as GuildMessageEvent
from nonebot.adapters.telegram.event import MessageEvent as TGMessageEvent

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")
from arclet.alconna.args import Args
from arclet.alconna.core import Alconna
from arclet.alconna.typing import CommandMeta
from nonebot_plugin_alconna import Match, AlconnaArg, on_alconna, AlconnaMatch
from nonebot_plugin_alconna.matcher import AlconnaMatcher
from nonebot_plugin_alconna.adapters import Image as AlcImage
from nonebot_plugin_saa import MessageFactory

from sora.log import logger
from sora.utils.requests import AsyncHttpx
from sora.utils.helpers import HandleCancellation
from sora.utils.utils import translate

analysis = on_alconna(
    Alconna(
        "图像鉴赏",
        Args["img?", AlcImage],
        meta=CommandMeta(
            description="让林汐为你的图片打发！",
            usage="/图像鉴赏",
            example="/图像鉴赏",
            compact=True,
        ),
    ),
    aliases={"分析图片", "鉴赏图片", "图片分析"},
    priority=50,
    block=True,
)


@analysis.handle()
async def image_analysis(
    matcher: AlconnaMatcher, image: Match[AlcImage] = AlconnaMatch("img")
):
    if image.available:
        matcher.set_path_arg("img", image.result)


@analysis.got_path(
    "img", prompt="请发送需要分析的图片", parameterless=[HandleCancellation("已取消")]
)
async def get_image(state: T_State, image: AlcImage = AlconnaArg("img")):
    if image.url:
        state["img"] = image.url
    else:
        state["img"] = image.id


@analysis.handle()
async def analysis_handle(
    bot: V11Bot | GuildBot | TGBot,
    event: V11MessageEvent | GuildMessageEvent | TGMessageEvent,
    state: T_State,
):
    await MessageFactory("正在分析图像, 请稍等……").send(at_sender=True)

    img = state.get("img")
    if img:
        try:
            if isinstance(event, TGMessageEvent) and isinstance(bot, TGBot):
                res = await bot.get_file(file_id=img)
                file_path = cast(str, res.file_path)
                url = f"{bot.bot_config.api_server}file/bot{bot.bot_config.token}/{file_path}"
            elif isinstance(event, V11MessageEvent):
                url = img
            else:
                url = f"https://{img}"
            result = await savor_image(url)
        except Exception as e:
            logger.error("图像鉴赏", f"分析图像失败：{e}")
            await MessageFactory("分析失败, 请稍后重试").send(reply=True)
            await analysis.finish()

        msg = ", ".join(
            i["label"] for i in result if not i["label"].startswith("rating:")
        )
        translation_msg = await translate(msg, type="EN2ZH_CN")
        await MessageFactory(translation_msg).send(reply=True)
    await analysis.finish()


def RandomString():
    characters = string.ascii_lowercase + string.digits
    return "".join(random.choices(characters, k=10))


class Confidence(TypedDict):
    label: str
    confidence: float


async def savor_image(img_url: str) -> list[Confidence]:
    logger.info("图像鉴赏", f"分析图片：{img_url}")
    res = await AsyncHttpx.get(img_url)
    if res.is_error:
        raise NetworkError("无法获取此图像")

    image = Image.open(BytesIO(res.content)).convert("RGB")
    image.save(imageData := BytesIO(), format="jpeg")
    img_b64 = base64.b64encode(imageData.getvalue()).decode()

    session_hash = RandomString()
    data = (
        '{"data":["data:image/jpeg;base64,'
        + img_b64
        + '",0.5],"event_data":null,"fn_index":1,"session_hash":"'
        + session_hash
        + '"}'
    )
    try:
        async with connect("wss://hysts-deepdanbooru.hf.space/queue/join") as websocket:
            greeting = await websocket.recv()
            await websocket.send('{"fn_index":1,"session_hash":"' + session_hash + '"}')
            greeting = await websocket.recv()
            greeting = await websocket.recv()
            await websocket.send(data)
            greeting = await websocket.recv()
            greeting = await websocket.recv()
            if "process_completed" in str(greeting):
                return json.loads(greeting)["output"]["data"][0]["confidences"]
            else:
                raise ValueError("分析出错")
    except Exception as e:
        raise NetworkError("网络出错") from e
