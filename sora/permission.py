from typing import Any

from nonebot.internal.adapter.event import Event
from nonebot.internal.permission import Permission as Permission

from sora.database import User


async def get_admin_list() -> list[tuple[Any, ...]]:
    """
    获取权限为 `Bot管理员` 的所有用户ID
    """
    return await User.filter(permission="ADMIN").values_list("uid", flat=True)


async def get_helper_list() -> list[tuple[Any, ...]]:
    """
    获取所有拥有 `Bot协助者` 权限的用户ID
    """
    return await User.filter(permission="HELPER").values_list("uid", flat=True)


class BotAdminUser:
    """检查当前事件是否是消息事件且属于 Bot管理员"""

    __slots__ = ()

    def __repr__(self) -> str:
        return "BotAdminUser()"

    async def __call__(self, event: Event) -> bool:
        try:
            uid = (await User.get_user_by_event(event)).uid
        except Exception:
            return False

        admin_list: list[tuple[Any, ...]] = await get_admin_list()
        if uid in admin_list:
            return True
        else:
            return False


class BotHelperUser:
    """检查当前事件是否是消息事件且属于 Bot协助者"""

    __slots__ = ()

    def __repr__(self) -> str:
        return "BotHelperUser()"

    async def __call__(self, event: Event) -> bool:
        try:
            uid = (await User.get_user_by_event(event)).uid
        except Exception:
            return False

        helper_list: list[tuple[Any, ...]] = await get_helper_list()
        if uid in helper_list:
            return True
        else:
            return False


ADMIN: Permission = Permission(BotAdminUser())
"""Bot 管理员"""
HELPER: Permission = Permission(BotHelperUser())
"""Bot 协助者"""
