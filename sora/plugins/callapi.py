import json
import traceback
from typing import Any, cast
from contextlib import suppress
from dataclasses import dataclass
from collections.abc import Iterable

from PIL import Image
from pydantic import BaseModel
from pygments import highlight
from pygments.style import Style
from nonebot.params import CommandArg
from nonebot import require, on_command
from bbcode import Parser as BBCodeParser
from nonebot.plugin import PluginMetadata
from pil_utils import BuildImage, Text2Image
from pygments.lexers import get_lexer_by_name
from pil_utils.fonts import DEFAULT_FALLBACK_FONTS
from pygments.formatters.bbcode import BBCodeFormatter
from nonebot.matcher import Matcher, current_bot, current_event
from nonebot.internal.adapter import Bot, Message, MessageSegment

require("nonebot_plugin_saa")
from nonebot_plugin_saa import MessageFactory
from nonebot_plugin_saa import Image as SAAImage

from sora.log import logger
from sora.permission import BOT_HELPER

__plugin_meta__ = PluginMetadata(
    name="CallAPI",
    description="使用指令来调用 Bot 的 API",
    usage="/callapi <API>\n[传入参数]",
    extra={"author": "student_2333", "priority": 10},
)


CODE_FONTS = [
    "JetBrains Mono",
    "Cascadia Mono",
    "Segoe UI Mono",
    "Liberation Mono",
    "Menlo",
    "Monaco",
    "Consolas",
    "Roboto Mono",
    "Courier New",
    "Courier",
    "Microsoft YaHei UI",
    *DEFAULT_FALLBACK_FONTS,
]
PADDING = 25

bbcode_parser = BBCodeParser()


@dataclass()
class Codeblock:
    lang: str | None
    content: str


def item_to_plain_text(item: str | Codeblock) -> str:
    parsed: list[tuple[int, str | None, dict | None, str]] = bbcode_parser.tokenize(
        f"```{item.lang or ''}\n{item.content}\n```" if isinstance(item, Codeblock) else item,
    )
    return "".join(
        [
            data
            for b_type, _, _, data in parsed
            if b_type == BBCodeParser.TOKEN_DATA or b_type == BBCodeParser.TOKEN_NEWLINE
        ],
    )


def format_plain_text(items: list[str | Codeblock]) -> str:
    return "\n".join(item_to_plain_text(it) for it in items)


def item_to_image(item: str | Codeblock) -> Image.Image:
    item = item or "\n"

    is_codeblock = isinstance(item, Codeblock)
    background_color: str | None = None

    if not is_codeblock:
        formatted = item

    else:
        formatter = BBCodeFormatter()
        style: Style = formatter.style
        background_color = getattr(style, "background_color", None)

        formatted: str | None = None
        if item.lang:
            with suppress(Exception):
                lexer = get_lexer_by_name(item.lang)
                formatted = cast(str, highlight(item.content, lexer, formatter))

        if not formatted:
            formatted = item.content

    text_img = Text2Image.from_bbcode_text(
        formatted,
        fallback_fonts=CODE_FONTS,
    )

    if not is_codeblock:
        return text_img.to_image()

    block_size = (text_img.width + PADDING * 2, text_img.height + PADDING * 2)
    block_width, block_height = block_size

    build_img = BuildImage.new("RGBA", block_size, (255, 255, 255, 0))

    if background_color:
        build_img.draw_rounded_rectangle(
            (0, 0, block_width, block_height),
            radius=10,
            fill=background_color,
        )

    text_img.draw_on_image(build_img.image, (PADDING, PADDING))
    return build_img.image


def draw_image(items: list[str | Codeblock]) -> bytes:
    images = [item_to_image(it) for it in items]

    width = max(img.width for img in images)
    height = sum(img.height for img in images)
    bg = BuildImage.new(
        "RGBA",
        (width + PADDING * 2, height + PADDING * 2),
        (255, 255, 255),
    )

    y = PADDING
    for img in images:
        bg.paste(img, (PADDING, y), alpha=True)
        y += img.height

    return bg.convert("RGB").save("png").getvalue()


async def send_return(items: list[str | Codeblock]):
    event = current_event.get()
    bot = current_bot.get()
    adapter = bot.adapter.get_name()

    if adapter == "QQ Guild":
        logger.warning("CallAPI", "Error sending image to channel, fallback to plain text")
        await bot.send(event, format_plain_text(items))
    else:
        try:
            # via saa
            image = draw_image(items)
            await MessageFactory(SAAImage(image)).send(reply=True)
            await bot.send(event, format_plain_text(items))
        except Exception:
            logger.warning("CallAPI", "Error when sending image via saa, fallback to plain text")
            await bot.send(event, format_plain_text(items))


def cast_param_type(param: str) -> Any:
    if param.isdigit():
        return int(param)

    if param.replace(".", "", 1).isdigit():
        return float(param)

    if param.lower() in ("true", "false"):
        return param.lower() == "true"

    return param


def parse_args(params: str) -> tuple[str, dict[str, Any]]:
    lines = params.splitlines(keepends=False)
    api_name = lines[0].strip()
    param_lines = lines[1:]

    try:
        param_dict = json.loads("\n".join(param_lines))
    except Exception:
        param_dict = {}
        for line in param_lines:
            if "=" not in line:
                raise ValueError(
                    f"参数 `{line}` 格式错误，应为 name=param",
                )

            key, value = line.split("=", 1)
            param_dict[key.strip()] = cast_param_type(value.strip())

    return api_name, param_dict


HELP_ITEMS = [
    "[b]指令格式：[/b]",
    Codeblock(lang=None, content="callapi <API 名称>\n[传入参数]"),
    "关于传入参数的格式，请看下面的调用示例",
    "",
    "[b]调用示例：[/b]",
    "使用 name=value 格式（会自动推断类型）：",
    Codeblock(
        lang=None,
        content=(
            "callapi get_stranger_info\n" "[color=#008000][b]user_id[/b][/color]=[color=#666666]3076823485[/color]"
        ),
    ),
    "使用 JSON（可以多行）：",
    Codeblock(
        lang=None,
        content=(
            "callapi get_stranger_info\n"
            '{ [color=#008000][b]"user_id"[/b][/color]: [color=#666666]3076823485[/color] }'  # noqa: E501
        ),
    ),
]
HELP_TEXT = format_plain_text(HELP_ITEMS)


call_api_matcher = on_command(
    cmd="callapi",
    permission=BOT_HELPER,
    priority=10,
    block=True,
    state={
        "name": "CallApi",
        "description": "调用 Bot 的 API",
        "usage": "/callapi <API名称>\n[传入参数]",
        "priority": 10,
    },
)


@call_api_matcher.handle()
async def _(matcher: Matcher, bot: Bot, args: Message = CommandArg()):
    arg_txt = "".join(
        [txt if x.is_text() and (txt := x.data.get("text")) else str(x) for x in cast(Iterable[MessageSegment], args)],
    ).strip()

    if not arg_txt:
        await send_return(HELP_ITEMS)
        return

    try:
        api, params_dict = parse_args(arg_txt)
    except ValueError as e:
        await matcher.finish(e.args[0])
    except Exception:
        logger.warning("CallAPI", "参数解析错误")
        await matcher.finish("参数解析错误，请检查后台输出")

    ret_items = [
        f"[b]Bot:[/b] {bot.adapter.get_name()} {bot.self_id}",
        "",
        f"[b]API:[/b] {api}",
        "",
        "[b]Params:[/b]",
        Codeblock(
            lang="json",
            content=json.dumps(params_dict, ensure_ascii=False, indent=2),
        ),
        "",
        "[b]Result:[/b]",
    ]

    try:
        result = await bot.call_api(api, **params_dict)
    except Exception:
        formatted = traceback.format_exc().strip()
        ret_items.append("Call API Failed!")
        ret_items.append(Codeblock(lang="pytb", content=formatted))

    else:
        if isinstance(result, BaseModel):
            result = result.dict()

        content = None
        with suppress(Exception):
            content = json.dumps(result, ensure_ascii=False, indent=2)

        ret_items.append(
            Codeblock(
                lang="json" if content else None,
                content=content or str(result),
            ),
        )

    await send_return(ret_items)
