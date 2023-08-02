from typing import Annotated

from nonebot import require
from nonebot.params import Depends
from tortoise.expressions import F
from nonebot.message import event_postprocessor
from nonebot.adapters.qqguild import Bot as GuildBot
from nonebot.adapters.onebot.v11 import Bot as V11Bot
from nonebot.adapters.telegram.bot import Bot as TGBot

require("nonebot_plugin_saa")
from nonebot_plugin_saa import MessageFactory, PlatformTarget, extract_target

from sora.database import UserInfo
from sora.utils.user import (
    getUserInfo,
    calculate_exp_threshold,
)


@event_postprocessor
async def level_up(
    bot: V11Bot | GuildBot | TGBot,
    userInfo: Annotated[UserInfo, getUserInfo()],
    target: PlatformTarget = Depends(extract_target),
):
    user_id = userInfo.user_id
    if user_id is None:
        return
    user_level = userInfo.level
    user_exp = userInfo.exp
    exp_threshold = calculate_exp_threshold(user_level)

    if user_exp >= exp_threshold:
        await UserInfo.filter(user_id=user_id).update(
            level=F("level") + 1, exp=F("exp") - exp_threshold
        )
        await MessageFactory(
            f"🎉 经验值溢出，等级 + 1！\n当前等级：{user_level + 1}，经验值：{user_exp - exp_threshold}"
        ).send_to(  # noqa: E501(
            target, bot
        )
