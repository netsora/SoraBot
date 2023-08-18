import random
import datetime
from datetime import date

from nonebot import require
from nonebot.rule import to_me
from tortoise.expressions import F
from nonebot.plugin import PluginMetadata

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")
from arclet.alconna.core import Alconna
from arclet.alconna.typing import CommandMeta
from nonebot_plugin_alconna import on_alconna, AlcResult
from nonebot_plugin_saa import Text, Image, MessageFactory

from sora.database.models import UserSign
from sora.utils.user import get_user_avatar
from sora.database.rewards import Exp, Coin, Favor, EventReward

from sora.utils.annotated import UserInfo

from .utils import get_rank, get_user_rank, generate_progress_bar
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

rank = on_alconna(
    Alconna(
        "排行榜",
        meta=CommandMeta(
            description="排行榜",
            usage="@bot /排行榜",
            example="@bot /我的信息",
            compact=True,
        ),
    ),
    aliases={
        "硬币排行",
        "经验排行",
        "经验值排行",
        "好感度排行",
        "硬币排行榜",
        "经验值排行榜",
        "好感度排行榜",
    },
    rule=to_me(),
    priority=20,
    block=True,
)


@sign.handle()
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
    {msg}历史最高 {str(total_days+1)} 天\n
    ——————————————\n
    ۞≡==——☚◆☛——==≡۞\n
    ➢[金币+{sign_coin}]\n
            —— Now: {coin + sign_coin}\n
    ➢[好感+{sign_favor}]\n
            —— Now: {favor + sign_favor}\n
    ➢[经验+{sign_exp}]\n
            —— Now: {exp + sign_exp}\n
    ۞≡==——☚◆☛——==≡۞\n
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


@rank.handle()
async def rank_(userInfo: UserInfo, commands: AlcResult):
    command_result = commands.result.header_result

    if "硬币" in command_result:
        type = "coin"
        command = "硬币"
    elif "经验" in command_result:
        type = "exp"
        command = "经验值"
    elif "好感" in command_result:
        type = "favor"
        command = "好感度"
    else:
        type = "coin"
        command = "硬币"

    all_ranks = await get_rank(type)
    user_rank = await get_user_rank(userInfo.user_id, type)

    msg = ""

    for ranks, user in all_ranks.items():
        user_id = user["user_id"]
        user_name = user["user_name"]
        count = user["count"]
        msg += f"[{ranks}] {user_name}({user_id}):  {count}\n"

    await MessageFactory(
        f"""
{command}排行榜：
{msg}
----------
您当前{command}排行：第{user_rank}名
"""
    ).send(at_sender=True)
    await rank.finish()
