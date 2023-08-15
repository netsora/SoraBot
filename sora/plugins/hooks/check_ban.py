from typing import Annotated

from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException

from sora.log import logger
from sora.utils.user import getUserInfo
from sora.database import BanUser, UserInfo


@run_preprocessor
async def _(userInfo: Annotated[UserInfo, getUserInfo()]):
    user_id = userInfo.user_id
    is_ban = await BanUser.is_ban(user_id)
    if is_ban:
        logger.debug("封禁", f"用户 {user_id} 处于黑名单中")
        raise IgnoredException("用户处于黑名单中")
