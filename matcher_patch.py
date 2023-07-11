import re
from contextlib import AsyncExitStack
from typing import Set, Tuple, Union, Optional

from nonebot.log import logger
from nonebot.internal.adapter import Bot, Event
from nonebot.adapters.qqguild import log as guildlog
from nonebot.adapters.onebot.v11 import log as v11log
from nonebot.typing import T_State, T_DependencyCache
from nonebot.exception import StopPropagation, SkippedException
from nonebot.adapters.qqguild import MessageEvent as GuildMessageEvent
from nonebot.adapters.onebot.v11 import MessageEvent as V11MessageEvent
from nonebot import on_regex, on_command, on_keyword, on_endswith, on_startswith
from nonebot.matcher import (
    Matcher,
    current_bot,
    current_event,
    current_handler,
    current_matcher,
)

"""
通过猴子补丁，干掉一些log，并为nonebot的部分matcher注入其命令到默认state中
"""


async def simple_run(
    self: Matcher,
    bot: Bot,
    event: Event,
    state: T_State,
    stack: Optional[AsyncExitStack] = None,
    dependency_cache: Optional[T_DependencyCache] = None,
):
    logger.debug(
        f"{self} run with incoming args: "
        f"bot={bot}, event={event!r}, state={state!r}"
    )
    b_t = current_bot.set(bot)
    e_t = current_event.set(event)
    m_t = current_matcher.set(self)
    try:
        # Refresh preprocess state
        self.state.update(state)

        while self.handlers:
            handler = self.handlers.pop(0)
            current_handler.set(handler)
            logger.debug(f"Running handler {handler}")
            try:
                await handler(
                    matcher=self,
                    bot=bot,
                    event=event,
                    state=self.state,
                    stack=stack,
                    dependency_cache=dependency_cache,
                )
            except SkippedException:
                logger.debug(f"Handler {handler} skipped")
    except StopPropagation:
        self.block = True
    finally:
        logger.debug(f"{self} running complete")
        current_bot.reset(b_t)
        current_event.reset(e_t)
        current_matcher.reset(m_t)


def on_command_(cmd: Union[str, Tuple[str, ...]], state: dict = None, *args, **kwargs):
    if state is None:
        state = {}
    if "pm_name" not in state:
        state["pm_name"] = cmd if isinstance(cmd, str) else cmd[0]
    return on_command(cmd=cmd, state=state, _depth=1, *args, **kwargs)


def on_endswith_(msg: Union[str, Tuple[str, ...]], state: dict = None, *args, **kwargs):
    if state is None:
        state = {}
    if "pm_name" not in state:
        state["pm_name"] = msg if isinstance(msg, str) else msg[0]
    return on_endswith(msg=msg, state=state, _depth=1, *args, **kwargs)


def on_startswith_(
    msg: Union[str, Tuple[str, ...]], state: dict = None, *args, **kwargs
):
    if state is None:
        state = {}
    if "pm_name" not in state:
        state["pm_name"] = msg if isinstance(msg, str) else msg[0]
    return on_startswith(msg=msg, state=state, _depth=1, *args, **kwargs)


def on_regex_(pattern: str, state: dict = None, *args, **kwargs):
    if state is None:
        state = {}
    if "pm_name" not in state:
        state["pm_name"] = pattern
    return on_regex(pattern=pattern, state=state, _depth=1, *args, **kwargs)


def on_keyword_(keywords: Set[str], state: dict = None, *args, **kwargs):
    if state is None:
        state = {}
    if "pm_name" not in state:
        state["pm_name"] = list(keywords)[0]
    return on_keyword(keywords=keywords, state=state, _depth=1, *args, **kwargs)


def _check_nickname(bot: Bot, event: Union[V11MessageEvent, GuildMessageEvent]) -> None:
    """检查消息开头是否存在昵称，去除并赋值 `event.to_me`。

    参数:
        bot: Bot 对象
        event: MessageEvent 对象
    """
    first_msg_seg = event.message[0]
    if first_msg_seg.type != "text":
        return

    if nicknames := set(filter(lambda n: n, bot.config.nickname)):
        # check if the user is calling me with my nickname
        nickname_regex = "|".join(nicknames)
        first_text = first_msg_seg.data["text"]

        if m := re.search(
            rf"^({nickname_regex})([\s,，]*|$)", first_text, re.IGNORECASE
        ):
            nickname = m[1]
            if isinstance(event, V11MessageEvent):
                v11log("DEBUG", f"User is calling me {nickname}")
            elif isinstance(event, GuildMessageEvent):
                guildlog("DEBUG", f"User is calling me {nickname}")
            event.to_me = True
            # first_msg_seg.data["text"] = first_text[m.end():]


Matcher.simple_run = simple_run
