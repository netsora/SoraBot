from contextlib import AsyncExitStack

import nonebot
from nonebot.log import logger
from nonebot.internal.adapter import Bot, Event
from nonebot.typing import T_State, T_DependencyCache
from nonebot.exception import StopPropagation, SkippedException
from nonebot import on_regex, on_command, on_keyword, on_endswith, on_startswith
from nonebot.matcher import Matcher, current_bot, current_event, current_handler, current_matcher

"""
通过猴子补丁，干掉一些log，并为nonebot的部分matcher注入其命令到默认state中
"""


async def simple_run(
    self: Matcher,
    bot: Bot,
    event: Event,
    state: T_State,
    stack: AsyncExitStack | None = None,
    dependency_cache: T_DependencyCache | None = None,
):
    logger.debug(f"{self} run with incoming args: " f"bot={bot}, event={event!r}, state={state!r}")
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


def on_command_(cmd: str | tuple[str, ...], state: dict = {}, *args, **kwargs):
    if state is None:
        state = {}
    if "name" not in state:
        state["name"] = cmd if isinstance(cmd, str) else cmd[0]
    return on_command(cmd=cmd, state=state, _depth=1, *args, **kwargs)


def on_endswith_(msg: str | tuple[str, ...], state: dict = {}, *args, **kwargs):
    if state is None:
        state = {}
    if "name" not in state:
        state["name"] = msg if isinstance(msg, str) else msg[0]
    return on_endswith(msg=msg, state=state, _depth=1, *args, **kwargs)


def on_startswith_(msg: str | tuple[str, ...], state: dict = {}, *args, **kwargs):
    if state is None:
        state = {}
    if "name" not in state:
        state["name"] = msg if isinstance(msg, str) else msg[0]
    return on_startswith(msg=msg, state=state, _depth=1, *args, **kwargs)


def on_regex_(pattern: str, state: dict = {}, *args, **kwargs):
    if state is None:
        state = {}
    if "name" not in state:
        state["name"] = pattern
    return on_regex(pattern=pattern, state=state, _depth=1, *args, **kwargs)


def on_keyword_(keywords: set[str], state: dict = {}, *args, **kwargs):
    if state is None:
        state = {}
    if "name" not in state:
        state["name"] = list(keywords)[0]
    return on_keyword(keywords=keywords, state=state, _depth=1, *args, **kwargs)


Matcher.simple_run = simple_run
nonebot.on_command = on_command_
nonebot.on_regex = on_regex_
nonebot.on_startswith = on_startswith_
nonebot.on_endswith = on_endswith_
nonebot.on_keyword = on_keyword_
