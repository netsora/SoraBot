import random
import string
import datetime

from nonebot.adapters.qqguild import MessageEvent as GuildMessageEvent
from nonebot.adapters.onebot.v11 import MessageEvent as V11MessageEvent
from nonebot.adapters.telegram.event import MessageEvent as TGMessageEvent

from sora.database.models import UserBind


def generate_id():
    """生成用户ID"""
    current_time = datetime.datetime.now().strftime("%Y%m%d")  # 获取当前日期
    random_number = random.randint(10, 99)  # 生成一个随机数
    if random_number < 10:
        random_number = "0" + str(random_number)
    user_id: str = f"{current_time}{random_number}"  # 结合日期和随机数生成ID
    return user_id


def generate_password(length=10, chars=string.ascii_letters + string.digits):
    """生成用户密码"""

    return "".join([random.choice(chars) for i in range(length)])


async def get_user_id(event: V11MessageEvent | GuildMessageEvent | TGMessageEvent):
    """
    通过 平台ID 获取 用户ID

    :param event:
    :return: user_id

    已支持的平台:

    * onebot_v11
    * qqguild
    * telegram
    """
    event_user_id = event.get_user_id()
    if isinstance(event, V11MessageEvent):
        user_bind_info = await UserBind.get_or_none(user_qq_id=event_user_id).values_list(
            "user_id",
            "user_qq_id",
            "user_qqguild_id",
            "discord_id",
            "telegram_id",
            "bilibili_id",
            "arcaea_id",
            "phigros_id",
        )
    elif isinstance(event, GuildMessageEvent):
        user_bind_info = await UserBind.get_or_none(user_qqguild_id=event_user_id).values_list(
            "user_id",
            "user_qq_id",
            "user_qqguild_id",
            "discord_id",
            "telegram_id",
            "bilibili_id",
            "arcaea_id",
            "phigros_id",
        )
    else:
        user_bind_info = await UserBind.get_or_none(telegram_id=event_user_id).values_list(
            "user_id",
            "user_qq_id",
            "user_qqguild_id",
            "discord_id",
            "telegram_id",
            "bilibili_id",
            "arcaea_id",
            "phigros_id",
        )
    user_id = user_bind_info[0]

    return user_id


async def get_user_login_list(event: V11MessageEvent | GuildMessageEvent | TGMessageEvent):
    """
    通过 用户ID 获取 登录信息

    :param event:
    :return: user_id

    已支持的平台:

    * onebot_v11
    * qqguild
    * telegram

    可获取的平台：
    * QQ
    * QQ频道
    * discord
    * telegram
    * bilibili
    * arcaea
    * phigros
    """
    event_user_id = event.get_user_id()
    if isinstance(event, V11MessageEvent):
        user_bind_info = await UserBind.get_or_none(user_qq_id=event_user_id).values_list(
            "user_id",
            "user_qq_id",
            "user_qqguild_id",
            "discord_id",
            "telegram_id",
            "bilibili_id",
            "arcaea_id",
            "phigros_id",
        )
    elif isinstance(event, GuildMessageEvent):
        user_bind_info = await UserBind.get_or_none(user_qqguild_id=event_user_id).values_list(
            "user_id",
            "user_qq_id",
            "user_qqguild_id",
            "discord_id",
            "telegram_id",
            "bilibili_id",
            "arcaea_id",
            "phigros_id",
        )
    else:
        user_bind_info = await UserBind.get_or_none(telegram_id=event_user_id).values_list(
            "user_id",
            "user_qq_id",
            "user_qqguild_id",
            "discord_id",
            "telegram_id",
            "bilibili_id",
            "arcaea_id",
            "phigros_id",
        )
    login_list = user_bind_info

    return login_list
