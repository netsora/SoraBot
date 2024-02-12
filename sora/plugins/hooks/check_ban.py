from nonebot.adapters import Bot, Event
from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException

from sora.log import logger
from sora.database import Ban, User


@run_preprocessor
async def _(bot: Bot, event: Event):
    platform = bot.adapter.get_name()
    pid = event.get_user_id()
    if await User.check_exists(platform, pid):
        uid = (await User.get_user_by_pid(pid)).uid
        is_ban = await Ban.is_banned(uid)
        if is_ban:
            logger.debug(f"用户 {uid} 处于黑名单中")
            raise IgnoredException("用户处于黑名单中")
