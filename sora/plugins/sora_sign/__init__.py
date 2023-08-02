import random
import datetime
from datetime import date
from typing import Annotated

from nonebot import require
from nonebot.rule import to_me
from tortoise.expressions import F
from nonebot.plugin import PluginMetadata

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")
from arclet.alconna.core import Alconna
from arclet.alconna.typing import CommandMeta
from nonebot_plugin_alconna import on_alconna
from nonebot_plugin_saa import Text, Image, MessageFactory

from sora.config import ConfigManager
from sora.database.models import UserInfo, UserSign
from sora.utils.user import getUserInfo, get_user_avatar

from .utils import generate_progress_bar

CoinRewards = ConfigManager.get_config("Award")["sign"][0]
JrrpRewards = ConfigManager.get_config("Award")["sign"][1]
ExpRewards = ConfigManager.get_config("Award")["sign"][2]

__sora_plugin_meta__ = PluginMetadata(
    name="签到",
    description="今天有想林汐嘛?",
    usage="""
    签到：/签到
    个人信息：/我的信息
    """,
    extra={"author": "KomoriDev", "priority": 20},
)


sign = on_alconna(
    Alconna(
        "签到",
        meta=CommandMeta(
            description="每日打卡",
            usage="@bot /签到",
            example="@bot /签到",
            compact=True,
        ),
    ),
    rule=to_me(),
    priority=20,
    block=True,
)

info = on_alconna(
    Alconna(
        "我的信息",
        meta=CommandMeta(
            description="查询我的等级经验信息。",
            usage="@bot /我的信息",
            example="@bot /我的信息",
            compact=True,
        ),
    ),
    aliases={"i"},
    rule=to_me(),
    priority=20,
    block=True,
)


@sign.handle()
async def sign_(userInfo: Annotated[UserInfo, getUserInfo()]):
    user_id = userInfo.user_id

    if user_id is None:
        await MessageFactory("该账号暂未注册林汐账户，请先发送 [/注册] ").send(at_sender=True)
        await sign.finish()
    user_sign = await UserSign.get_or_none(user_id=user_id).values(
        "total_days", "continuous_days", "last_day"
    )

    exp: int = userInfo.exp
    coin: int = userInfo.coin
    jrrp: int = userInfo.jrrp

    sign_coin: int = (
        random.randint(CoinRewards[0], CoinRewards[1]) if CoinRewards is not None else 0
    )
    sign_jrrp: int = JrrpRewards if JrrpRewards is not None else 0
    sign_exp: int = ExpRewards if ExpRewards is not None else 0

    total_days: int = user_sign["total_days"]
    last_sign_date: date = user_sign["last_day"]
    continuous_days: int = user_sign["continuous_days"]

    current_date = datetime.date.today()

    if current_date == last_sign_date:
        msg = "您今日已经签到过了，不可重复签到"
        await MessageFactory(msg).send(at_sender=True)
        await sign.finish()

    # 判断是否连续签到
    if last_sign_date is None or (current_date - last_sign_date).days == 1:
        msg = f"你当前连续签到 {str(continuous_days + 1)} 天，额外奖励 5 枚硬币。"
        sign_coin += 5
        await UserSign.filter(user_id=user_id).update(
            continuous_days=F("continuous_days") + 1
        )
    else:
        msg = "你当前连续签到 0 天，"
        await UserSign.filter(user_id=user_id).update(continuous_days=0)

    await UserSign.filter(user_id=user_id).update(
        total_days=total_days + 1, last_day=current_date
    )
    await UserInfo.filter(user_id=user_id).update(
        exp=exp + sign_exp, coin=coin + sign_coin, jrrp=jrrp + sign_jrrp
    )

    await MessageFactory(
        f"""
    签到成功！
    {msg}历史最高 {str(total_days+1)} 天\n
    ——————————————\n
    ۞≡==——☚◆☛——==≡۞\n
    ➢[金币+{sign_coin}]\n
            —— Now: {coin + sign_coin}\n
    ➢[好感+{sign_jrrp}]\n
            —— Now: {jrrp + sign_jrrp}\n
    ➢[经验+{sign_exp}]\n
            —— Now: {exp + sign_exp}\n
    ۞≡==——☚◆☛——==≡۞\n
    —————————————
    """
    ).send(at_sender=True)


@info.handle()
async def info_(userInfo: Annotated[UserInfo, getUserInfo()]):
    user_id = userInfo.user_id
    if user_id is None:
        await MessageFactory("该账号未注册，请先发送 [/注册] 注册林汐账户").send(at_sender=True)
        await info.finish()

    user_avatar = get_user_avatar(user_id)
    user_name = userInfo.user_name
    user_level = userInfo.level
    user_exp = userInfo.exp
    user_coin = userInfo.coin
    progress_bar, progress_text = generate_progress_bar(
        user_level=user_level, user_exp=user_exp
    )

    if user_avatar is None:
        msg = MessageFactory(
            f"个人信息\n用户名：{user_name}\nLv.{str(user_level)}: {progress_bar}\n ↳ {progress_text}\n硬币：{user_coin} 个"  # noqa: E501
        )
    else:
        msg = MessageFactory(
            [
                Image(user_avatar),
                Text(
                    f"\n个人信息\n用户名：{user_name}\nLv.{str(user_level)}: {progress_bar}\n ↳ {progress_text}\n硬币：{user_coin} 个"  # noqa: E501
                ),
            ]
        )
    await msg.send(at_sender=True)
    await info.finish()
