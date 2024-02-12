from nonebot import require
from nonebot.params import Depends
from tortoise.expressions import F
from nonebot.message import run_postprocessor
from nonebot.internal.adapter import Bot, Event

require("nonebot_plugin_saa")
from nonebot_plugin_saa import MessageFactory, PlatformTarget, extract_target

from sora.database import User
from sora.utils.annotated import UserInfo
from sora.plugins.sign.config import GameConfig
from sora.plugins.sign.utils import calc_exp_threshold

level_config = (GameConfig.load_config("game")).level


@run_postprocessor
async def level_up(
    bot: Bot,
    event: Event,
    userInfo: UserInfo,
    target: PlatformTarget = Depends(extract_target),
):
    if not await User.check_exists(bot.type, event.get_user_id()):
        return

    uid = userInfo.uid
    user_level = userInfo.level
    user_exp = userInfo.exp
    exp_threshold = calc_exp_threshold(user_level)

    if user_exp >= exp_threshold:
        await User.filter(uid=uid).update(
            level=F("level") + 1, exp=F("exp") - exp_threshold
        )
        await MessageFactory(
            f"🎉 经验值溢出，等级 + 1！\n当前等级：{user_level + 1}，经验值：{user_exp - exp_threshold}"
        ).send_to(target, bot)
