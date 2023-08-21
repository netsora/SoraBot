import random
import datetime
from datetime import date

from nonebot import require
from nonebot.rule import to_me
from tortoise.expressions import F
from nonebot.plugin import PluginMetadata
from nonebot.internal.adapter import Event

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")
from arclet.alconna.args import Args
from arclet.alconna.base import Option
from arclet.alconna.core import Alconna
from arclet.alconna.typing import CommandMeta
from nonebot_plugin_alconna.adapters import At
from nonebot_plugin_alconna import Match, on_alconna, AlconnaMatch
from nonebot_plugin_saa import Text, Image, MessageFactory

from sora.database.models import UserSign
from sora.utils.user import get_bind_info, get_user_avatar, get_user_name
from sora.database.rewards import Exp, Coin, Favor, EventReward

from sora.utils.annotated import UserInfo

from .utils import generate_progress_bar
from .config import (
    base_exp as base_exp,
    max_level as max_level,
    cardinality as cardinality,
)

signEvent = EventReward(
    name="签到事件",
    description="第一次使用林汐",
    coin_reward=Coin(amount=[30, 60]),
    exp_reward=Exp(amount=100),
    favor_reward=Favor(amount=20),
)

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
        Option("info", Args["target?", At | int], alias={"信息"}, help_text="获取签到信息"),
        Option("rank", alias={"排行", "排行榜"}, help_text="当日签到排行榜"),
        Option("rank2", alias={"总排行", "排行榜"}, help_text="签到总排行"),
        meta=CommandMeta(
            description="每日打卡",
            usage="签到：@bot /签到\n签到信息：@bot /签到信息 [At]\n当日签到排行：@bot /签到排行",
            example="@bot /签到",
            compact=True,
        ),
    ),
    aliases={"sign"},
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


@sign.assign("$main")
async def sign_(userInfo: UserInfo):
    user_id = userInfo.user_id

    if user_id is None:
        await MessageFactory("该账号暂未注册林汐账户，请先发送 [/注册] ").send(at_sender=True)
        await sign.finish()
    user_sign = await UserSign.get_or_none(user_id=user_id).values(
        "total_days", "continuous_days", "last_day"
    )

    exp: int = userInfo.exp
    coin: int = userInfo.coin
    favor: int = userInfo.favor

    sign_coin = random.randint(signEvent.coin_reward[0], signEvent.coin_reward[1])
    sign_favor = signEvent.favor_reward.amount
    sign_exp = signEvent.exp_reward.amount

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
        exp=exp + sign_exp, coin=coin + sign_coin, favor=favor + sign_favor
    )

    await MessageFactory(
        f"""
    签到成功！
    {msg}历史最高 {str(total_days+1)} 天
    ——————————————
    ۞≡==——☚◆☛——==≡۞
    ➢[金币+{sign_coin}]
            —— Now: {coin + sign_coin}
    ➢[好感+{sign_favor}]
            —— Now: {favor + sign_favor}
    ➢[经验+{sign_exp}]
            —— Now: {exp + sign_exp}
    ۞≡==——☚◆☛——==≡۞
    —————————————
    """
    ).send(at_sender=True)


@info.handle()
async def info_(userInfo: UserInfo):
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
            f"个人信息\nID：{user_id}\n用户名：{user_name}\nLv.{str(user_level)}: {progress_bar}\n ↳ {progress_text}\n硬币：{user_coin} 个"  # noqa: E501
        )
    else:
        msg = MessageFactory(
            [
                Image(user_avatar),
                Text(
                    f"\n个人信息\nID：{user_id}\n用户名：{user_name}\nLv.{str(user_level)}: {progress_bar}\n ↳ {progress_text}\n硬币：{user_coin} 个"  # noqa: E501
                ),
            ]
        )
    await msg.send(at_sender=True)
    await info.finish()


@sign.assign("info")
async def sign_info(
    event: Event, userInfo: UserInfo, target: Match[At | str] = AlconnaMatch("target")
):
    if target.available:
        if isinstance(target.result, At):
            target_id = (await get_bind_info(event, target.result.target)).user_id
        else:
            target_id = target.result
        call = await get_user_name(target_id)
    else:
        target_id = userInfo.user_id
        call = "您"

    total_days, continuous_days = await UserSign.get_user_sign_info(target_id)

    await MessageFactory(f"{call}当前连续签到 {continuous_days} 天，累计 {total_days} 天").send(
        at_sender=True
    )
    await sign.finish()


@sign.assign("rank")
async def today_rank():
    result = await UserSign.get_today_rank()

    msg = ""

    for i, info in enumerate(result, start=1):
        user_id = info.user_id
        user_name = await get_user_name(user_id)
        msg += f"\n[{i}] {user_name}({user_id}) 共签到 {info.total_days} 天，当前已连续签到 {info.continuous_days} 天"

    await MessageFactory(msg).send(at_sender=True)
    await sign.finish()


@sign.assign("rank2")
async def total_rank():
    result = await UserSign.get_total_rank()

    msg = ""

    for i, info in enumerate(result, start=1):
        user_id = info.user_id
        user_name = await get_user_name(user_id)
        msg += f"\n[{i}] {user_name}({user_id}) 共签到 {info.total_days} 天，当前已连续签到 {info.continuous_days} 天"

    await MessageFactory(msg).send(at_sender=True)
    await sign.finish()
