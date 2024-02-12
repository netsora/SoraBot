from functools import wraps
from collections import defaultdict
from collections.abc import Callable
from typing import Any, TypeVar, ParamSpec, cast

from nonebot import get_driver
from nonebot.typing import T_BotConnectionHook, T_BotDisconnectionHook

R = TypeVar("R")
P = ParamSpec("P")

AnyCallable = Callable[..., Any]

_backlog_hooks = defaultdict(list)

_hook_installed = False


def backlog_hook(hook: Callable[P, R]) -> Callable[P, R]:
    """在初始化之前暂存钩子"""

    @wraps(hook)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        if _hook_installed:
            return hook(*args, **kwargs)
        try:
            _backlog_hooks[hook].append(args[0])
            return cast(R, args[0])
        except IndexError:
            return hook(*args, **kwargs)

    return wrapper


def install_hook() -> None:
    """将暂存的钩子安装"""
    for hook, funcs in _backlog_hooks.items():
        while funcs:
            func = funcs.pop(0)
            hook(func)
    global _hook_installed  # noqa: PLW0603
    _hook_installed = True


@backlog_hook
def on_startup(func: AnyCallable | None = None, pre: bool = False) -> AnyCallable:
    """在 `SoraBot` 启动时有序执行"""
    if func is None:
        return lambda f: on_startup(f, pre=pre)
    if pre:
        _backlog_hooks[on_startup.__wrapped__].insert(0, func)
        return func
    return get_driver().on_startup(func)


@backlog_hook
def on_shutdown(func: AnyCallable) -> AnyCallable:
    """在 `SoraBot` 停止时有序执行"""
    return get_driver().on_shutdown(func)


@backlog_hook
def on_bot_connect(func: T_BotConnectionHook) -> T_BotConnectionHook:
    """
    在 bot 成功连接到 `SoraBot` 时执行。
    """
    return get_driver().on_bot_connect(func)


@backlog_hook
def on_bot_disconnect(func: T_BotDisconnectionHook) -> T_BotDisconnectionHook:
    """
    在 bot 与 `SoraBot` 连接断开时执行。
    """
    return get_driver().on_bot_disconnect(func)
