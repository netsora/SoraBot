from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException

from sora.log import logger
from sora.database import BanUser
from sora.utils.annotated import UserInfo


@run_preprocessor
async def _(userInfo: UserInfo):
    user_id = userInfo.user_id
    is_ban = await BanUser.is_ban(user_id)
    if is_ban:
        logger.debug("封禁", f"用户 {user_id} 处于黑名单中")
        raise IgnoredException("用户处于黑名单中")
