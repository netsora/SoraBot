import re

from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Depends, EventMessage


def extract_image_urls(message: Message) -> list[str]:
    """提取消息中的图片链接

    参数:
        message: 消息对象

    返回:
        图片链接列表
    """
    return [
        segment.data["url"]
        for segment in message
        if (segment.type == "image") and ("url" in segment.data)
    ]


CHINESE_CANCELLATION_WORDS = {"算", "别", "不", "停", "取消"}
CHINESE_CANCELLATION_REGEX_1 = re.compile(r"^那?[算别不停]\w{0,3}了?吧?$")
CHINESE_CANCELLATION_REGEX_2 = re.compile(r"^那?(?:[给帮]我)?取消了?吧?$")


def is_cancellation(message: Message | str) -> bool:
    """判断消息是否表示取消

    参数:
        message: 消息对象或消息文本

    返回:
        是否表示取消的布尔值
    """ """"""
    text = (
        message.extract_plain_text()
        if isinstance(message, Message)
        else message
    )
    return any(kw in text for kw in CHINESE_CANCELLATION_WORDS) and bool(
        CHINESE_CANCELLATION_REGEX_1.match(text)
        or CHINESE_CANCELLATION_REGEX_2.match(text)
    )


def HandleCancellation(cancel_prompt: str | None = None) -> bool:
    """检查消息是否表示取消`is_cancellation`的依赖注入版本

    参数:
        cancel_prompt: 当消息表示取消时发送给用户的取消消息
    """ """"""

    async def dependency(
        matcher: Matcher, message: Message = EventMessage()
    ) -> bool:
        cancelled = is_cancellation(message)
        if cancelled and cancel_prompt:
            await matcher.finish(cancel_prompt)
        return not cancelled

    return Depends(dependency)
