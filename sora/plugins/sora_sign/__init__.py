import random
import datetime
from datetime import date

from nonebot.rule import to_me
from tortoise.expressions import F
from nonebot import require, on_command
from nonebot.adapters.qqguild import MessageEvent as GuildMessageEvent

# from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import MessageEvent as V11MessageEvent
from nonebot.adapters.telegram.event import MessageEvent as TGMessageEvent

require("nonebot_plugin_saa")
from nonebot_plugin_saa import MessageFactory

from sora import config
from sora.utils.user import get_user_id
from sora.database.models import UserInfo, UserSign

config = config.Award

sign = on_command(
    cmd="签到",
    rule=to_me(),
    priority=20,
    block=True,
    state={
        "name": "sign",
        "description": "签到",
        "usage": "@bot /签到",
        "priority": 20,
    },
)

info = on_command(
    cmd="我的信息",
    aliases={"i"},
    rule=to_me(),
    priority=20,
    block=True,
    state={
        "name": "my_info",
        "description": "签到",
        "usage": "@bot /i",
        "priority": 20,
    },
)


@sign.handle()
async def sign_(event: V11MessageEvent | GuildMessageEvent | TGMessageEvent):
    user_id = await get_user_id(event)
    user_info = await UserInfo.get_or_none(user_id=user_id).values("level", "exp", "coin", "jrrp")
    user_sign = await UserSign.get_or_none(user_id=user_id).values("total_days", "continuous_days", "last_day")
    if user_id is None:
        await MessageFactory("该账号暂未注册林汐账户，请先发送 [/注册] ").send(at_sender=True)
        await sign.finish()

    # level: int = user_info["level"]
    exp: int = user_info["exp"]
    coin: int = user_info["coin"]
    jrrp: int = user_info["jrrp"]

    sign_coin: int = random.randint(config.Coin.sign[0], config.Coin.sign[1])
    sign_jrrp = config.Jrrp.sign
    sign_exp = config.Exp.sign

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
        await UserSign.filter(user_id=user_id).update(continuous_days=F("continuous_days") + 1)
    else:
        msg = "你当前连续签到 0 天，"
        await UserSign.filter(user_id=user_id).update(continuous_days=0)

    await UserSign.filter(user_id=user_id).update(total_days=total_days + 1, last_day=current_date)
    await UserInfo.filter(user_id=user_id).update(exp=exp + sign_exp, coin=coin + sign_coin, jrrp=jrrp + sign_jrrp)

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
