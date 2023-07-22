"""
林汐权限机制：

规则：user < bot_helper < bot_admin

说明：
    * bot_helper 包括所有的 bot_admin
    * bot_admin 是最高权限，同样拥有 bot_helper 的权限

例子：

`/重启` 指令只能由 bot_admin 触发
```python
reboot_cmd = on_command(
    cmd='重启',
    permission=BOT_ADMIN
)
```

`/重启` 指令可以由 bot_admin 和 bot_helper 触发
```python
reboot_cmd = on_command(
    cmd='重启',
    permission=BOT_HELPER
)

```
"""
from nonebot.internal.permission import Permission as Permission
from nonebot.adapters.qqguild import MessageEvent as GuildMessageEvent
from nonebot.adapters.onebot.v11 import MessageEvent as V11MessageEvent
from nonebot.adapters.telegram.event import MessageEvent as TGMessageEvent

from sora.utils.user import get_user_id
from sora.database.models import UserInfo


async def get_admin_list():
    """
    获取权限为 `Bot管理员` 的所有用户ID
    """
    admin_list = await UserInfo.filter(permission="bot_admin").values_list("user_id", flat=True)
    return admin_list


async def get_helper_list():
    """
    获取所有拥有 Bot协助者 权限的用户ID
    """
    admin_list = await get_admin_list()
    helper_list = await UserInfo.filter(permission="bot_helper").values_list("user_id", flat=True)
    helper_list = admin_list + helper_list
    return helper_list


class BotAdminUser:
    """检查当前事件是否是消息事件且属于 Bot管理员"""

    __slots__ = ()

    def __repr__(self) -> str:
        return "BotAdminUser()"

    async def __call__(self, event: V11MessageEvent | GuildMessageEvent | TGMessageEvent) -> bool:
        try:
            user_id = await get_user_id(event)
        except Exception:
            return False

        admin_list: list = await get_admin_list()
        if user_id in admin_list:
            return True
        else:
            return False


class BotHelperUser:
    """检查当前事件是否是消息事件且属于 Bot协助者"""

    __slots__ = ()

    def __repr__(self) -> str:
        return "BotHelperUser()"

    async def __call__(self, event: V11MessageEvent | GuildMessageEvent | TGMessageEvent) -> bool:
        try:
            user_id = await get_user_id(event)
        except Exception:
            return False

        helper_list: list = await get_helper_list()
        if user_id in helper_list:
            return True
        else:
            return False


BOT_ADMIN: Permission = Permission(BotAdminUser())
"""Bot 管理员"""
BOT_HELPER: Permission = Permission(BotHelperUser())
"""Bot 协助者（默认包含 Bot管理员，不需要重复配置）"""
